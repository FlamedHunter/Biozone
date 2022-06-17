from django.shortcuts import render, redirect
from wishlist.models import Wishlist, Wishlist_Item
from .forms import OrderForm
import datetime
from .models import Order, OrderProduct
# Create your views here.
def place_order(request):
    current_user = request.user
    # If the cart count is less than or equal to 0, then redirect back to shop
    wishlist_items = Wishlist_Item.objects.filter(user=current_user)
    wishlist_count = wishlist_items.count()
    if wishlist_count <= 0:
        return redirect('store')

    if request.method == 'POST':
        form = OrderForm(request.POST)
        if form.is_valid():
            # Store all the billing information inside Order table
            data = Order()
            data.user = current_user
            data.first_name = form.cleaned_data['first_name']
            data.last_name = form.cleaned_data['last_name']
            data.phone = form.cleaned_data['phone']
            data.email = form.cleaned_data['email']
            data.address_line = form.cleaned_data['address_line']
            data.state = form.cleaned_data['state']
            data.city = form.cleaned_data['city']
            data.order_note = form.cleaned_data['order_note']
            data.ip = request.META.get('REMOTE_ADDR')
            data.save()
            # Generate order number
            yr = int(datetime.date.today().strftime('%Y'))
            dt = int(datetime.date.today().strftime('%d'))
            mt = int(datetime.date.today().strftime('%m'))
            d = datetime.date(yr,mt,dt)
            current_date = d.strftime("%Y%m%d") 
            order_number = current_date + str(data.id)
            data.order_number = order_number
            data.save()

            # order = Order.objects.get(user=current_user, is_ordered=False, order_number=order_number)
            # context = {
            #     'order': order,
            #     'cart_items': wishlist_items,
            # }
            return redirect('checkout')
    else:
        return redirect('checkout')
