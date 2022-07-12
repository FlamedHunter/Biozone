from http.client import HTTPResponse
from django.shortcuts import render, redirect
from wishlist.models import Wishlist, Wishlist_Item
from .forms import OrderForm
import datetime
from instrument.models import Institute, Instrument
from .models import Order, OrderProduct
# Create your views here.
from django.template.loader import render_to_string
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.core.mail import EmailMessage


def place_order(request):
    current_user = request.user
    # If the cart count is less than or equal to 0, then redirect back to shop
    wishlist_items = Wishlist_Item.objects.filter(user=current_user)
    wishlist_count = wishlist_items.count()
    # print("wc",wishlist_count)
    if wishlist_count <= 0:
        return redirect('instrument')
    if request.method == 'POST':
        form = OrderForm(request.POST)
        if form.is_valid():
            order = Order()
            order.user = current_user
            order.first_name = form.cleaned_data['first_name']
            order.last_name = form.cleaned_data['last_name']
            order.phone = form.cleaned_data['phone']
            order.email = form.cleaned_data['email']
            order.address_line = form.cleaned_data['address_line']
            order.state = form.cleaned_data['state']
            order.city = form.cleaned_data['city']
            order.order_note = form.cleaned_data['order_note']
            order.ip = request.META.get('REMOTE_ADDR')
            order.save()
            # Generate order number
            yr = int(datetime.date.today().strftime('%Y'))
            dt = int(datetime.date.today().strftime('%d'))
            mt = int(datetime.date.today().strftime('%m'))
            d = datetime.date(yr,mt,dt)
            current_date = d.strftime("%Y%m%d") 
            order_number = current_date + str(order.id)
            order.order_number = order_number
            order.save()
            order = Order.objects.get(user=current_user, is_ordered=False, order_number=order_number)
            context = {
                'order': order,
                'wishlist_items': wishlist_items,
            }
            return render(request, 'orders/review_order.html', context)
    else:
        return redirect('checkout')

def review_order(request, order_number):
    order = Order.objects.get(user=request.user, is_ordered=False, order_number=order_number)
    order.is_ordered = True
    order.save()

    # Move the cart items to Order Product table
    wishlist_items = Wishlist_Item.objects.filter(user=request.user)
    for item in wishlist_items:
        orderproduct = OrderProduct()
        orderproduct.order_id = order.id
        orderproduct.user_id = request.user.id
        orderproduct.instrument_id = item.instrument_id
        orderproduct.ordered = True
        orderproduct.save()
    
        # Reduce the quantity of the sold products
        # instrument = Instrument.objects.get(id=item.instrument_id)
        # instrument.instrument_quantity -= 1
        # instrument.save()
    
    # Clear Wishlist
    Wishlist_Item.objects.filter(user=request.user).delete()

    # # Send order recieved email to customer
    mail_subject = 'Thank you for your order!'
    message = render_to_string('orders/order_recieved_email.html', {
        'user': request.user,
        'order': order,
    })
    to_email = request.user.email
    send_email = EmailMessage(mail_subject, message, to=[to_email])
    send_email.send()
    request.session['order_number'] = order_number
    return redirect('order_complete')

def order_complete(request):
    order_id = request.session['order_number']
    order_detail = OrderProduct.objects.filter(order__order_number=order_id)
    order = Order.objects.get(order_number=order_id)
    # order.status = 'Completed'
    # order.save()
    context = {
        'order_detail': order_detail,
        'order': order,
    }
    return render(request, 'orders/order_complete.html', context)


