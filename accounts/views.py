from email import message
from http.client import HTTPResponse
from django.utils.datastructures import MultiValueDictKeyError
from instrument.views import instrument
from .forms import RegistrationForm, UserForm, UserProfileForm
from .models import Account,  UserProfile, OtpLogin 
from instrumentmanager.models import Instrument_Manager
from django.contrib import messages, auth
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login as ologin
# Create your views here.
from django.contrib.sites.shortcuts import get_current_site
from django.template.loader import render_to_string
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_bytes
from django.contrib.auth.tokens import default_token_generator
from django.core.mail import EmailMessage
from wishlist.models import Wishlist, Wishlist_Item
from wishlist.views import _wishlist_id
from django.shortcuts import render, redirect, get_object_or_404
from django.core.exceptions import ObjectDoesNotExist
from instrument.models import Instrument
from django.db.models import Q
from category.models import Category
from institute.models import Institute
from django.template.defaultfilters import slugify
import random
from django.conf import settings
# from .models import Wishlist, Wishlist_Item
from orders.models import Order, OrderProduct


def register(request):
    if request.method == "POST":
        form = RegistrationForm(request.POST)
        if form.is_valid():
            first_name = form.cleaned_data["first_name"]
            last_name = form.cleaned_data["last_name"]
            phone_number = form.cleaned_data["phone_number"]
            email = form.cleaned_data["email"]
            affiliation = form.cleaned_data["affiliation"]
            password = form.cleaned_data["password"]
            username = email.split("@")[0]
            user = Account.objects.create_user(first_name=first_name, last_name=last_name, email=email, affiliation=affiliation,username=username,password=password)
            user.phone_number = phone_number
            user.save()

            # Creating Profile
            profile = UserProfile()
            profile.user_id = user.id
            profile.profile_picture = 'default/default-user.png'
            profile.save()    
            
            #Creating OTP Login Profile 
            otp = str(random.randint(1000,9999))
            otplogin = OtpLogin()
            otplogin.user = user
            otplogin.otp = otp
            otplogin.save()

            # USER ACTIVATION
            current_site = get_current_site(request)
            mail_subject = 'Please activate your account'
            message = render_to_string('accounts/account_email_verification.html', {
                'user': user,
                'domain': current_site,
                'uid': urlsafe_base64_encode(force_bytes(user.pk)),
                'token': default_token_generator.make_token(user),
            })
            to_email = email
            send_email = EmailMessage(mail_subject, message, to=[to_email])
            send_email.send()

            # messages.success(request, 'Registration Successful')
            # return redirect('login')
            return redirect('/accounts/login/?command=verification&email=' + email)
    else:
        form = RegistrationForm()
    context = {
        'form':form,
    }
    return render(request, 'accounts/register.html', context)
# ologin(request,user)
def login(request):
    if request.method == "POST":
        email = request.POST["email"]
        password = request.POST["password"]

        user = auth.authenticate(email=email, password=password)

        if user is not None:
            try:
                wishlist = Wishlist.objects.get(wishlist_id=_wishlist_id(request))
                is_wishlist_item_exists = Wishlist_Item.objects.filter(wishlist=wishlist).exists()
                if is_wishlist_item_exists:
                    wishlist_items = Wishlist_Item.objects.filter(wishlist=wishlist)
                    for item in wishlist_items:
                        item.user=user
                        item.save()
            except:
                pass
            auth.login(request, user)
            messages.success(request, "Logged in Successfully!")
            return redirect('dashboard')
        else:
            messages.error(request, "Invalid Login Credentials")
            return redirect('login')
    return render(request, 'accounts/login.html')

def send_otp_email(email,otp):
    # print(email)
    # print(otp)
    return None

def sendotp(request):
    # print("send", request.POST['email'])
    if request.method == 'POST':
        # print("p")
        email = request.POST['email']
        # print("email", email)
        otp = str(random.randint(1000,9999))
        # print(otp)
        user = Account.objects.get(email__exact=email)
        otp_user = get_object_or_404(OtpLogin, user=user)
        # otp_user = OtpLogin.objects.filter(user=user)    
        otp_user.otp = otp
        otp_user.save()  
        # Send Email
        msg = "OTP to Login is: " + otp
        send_email = EmailMessage("OTP", msg , to=[email])
        send_email.send()
        # send_otp_email(email,otp)
        request.session['email'] = email
        context = {'user':user,'email':email,}
        return redirect('otplogin')
        # return render(request, 'accounts/otplogin.html', context)
    # else:
    #     return redirect('sendotp')
    # send_otp_email(email,otp)
    # print("dd")
    return render(request, 'accounts/sendotp.html')

def otplogin(request):
    email = request.session['email']
    context = {'email':email}
    if request.method == 'POST':
        otp = request.POST.get('otp')
        user = Account.objects.get(email__exact=email)
        otp_user = get_object_or_404(OtpLogin, user=user)
        if otp==otp_user.otp:
            # print(user.username)
            auth.login(request, user)
            return redirect('dashboard')
        else:
            context = {'message' : 'Wrong OTP' , 'class' : 'danger','email':email}
            return render(request,'accounts/otplogin.html' , context)
    return render(request, 'accounts/otplogin.html',context)


@login_required(login_url = 'login')
def logout(request):
    auth.logout(request)
    messages.success(request, "You are logged out!")
    return redirect('login')

@login_required(login_url = 'login')
def activate(request, uidb64, token):
    try:
        uid = urlsafe_base64_decode(uidb64).decode()
        user = Account._default_manager.get(pk=uid)
    except(TypeError, ValueError, OverflowError, Account.DoesNotExist):
        user = None

    if user is not None and default_token_generator.check_token(user, token):
        user.is_active = True
        user.save()
        messages.success(request, 'Congratulations! Your account is activated.')
        return redirect('login')
    else:
        messages.error(request, 'Invalid activation link')
        return redirect('register')

def forgotPassword(request):
    if request.method == 'POST':
        email = request.POST['email']
        if Account.objects.filter(email=email).exists():
            user = Account.objects.get(email__exact=email)
            # Reset password email
            current_site = get_current_site(request)
            mail_subject = 'Reset Your Password'
            message = render_to_string('accounts/reset_password_email.html', {
                'user': user,
                'domain': current_site,
                'uid': urlsafe_base64_encode(force_bytes(user.pk)),
                'token': default_token_generator.make_token(user),
            })
            to_email = email
            send_email = EmailMessage(mail_subject, message, to=[to_email])
            send_email.send()

            messages.success(request, 'Password reset email has been sent to your email address.')
            return redirect('login')
        else:
            messages.error(request, 'Account does not exist!')
            return redirect('forgotPassword')
    return render(request, 'accounts/forgotPassword.html')

def resetpassword_validate(request, uidb64, token):
    try:
        uid = urlsafe_base64_decode(uidb64).decode()
        user = Account._default_manager.get(pk=uid)
    except(TypeError, ValueError, OverflowError, Account.DoesNotExist):
        user = None

    if user is not None and default_token_generator.check_token(user, token):
        request.session['uid'] = uid
        messages.success(request, 'Please reset your password')
        return redirect('resetPassword')
    else:
        messages.error(request, 'This link has been expired!')
        return redirect('login')

def resetPassword(request):
    if request.method == 'POST':
        password = request.POST['password']
        confirm_password = request.POST['confirm_password']

        if password == confirm_password:
            uid = request.session.get('uid')
            user = Account.objects.get(pk=uid)
            user.set_password(password)
            user.save()
            messages.success(request, 'Password reset successful')
            return redirect('login')
        else:
            messages.error(request, 'Password do not match!')
            return redirect('resetPassword')
    else:
        return render(request, 'accounts/resetPassword.html')


@login_required(login_url = 'login')
def dashboard(request):
    total_products = 0
    instrument_manager = Instrument_Manager.objects.filter(manager=request.user)
    for im in instrument_manager:
        inst = im.instrument
        total_products+=1
    # print(total_products) 
    userprofile = get_object_or_404(UserProfile, user=request.user)
    wishlist_items=[]
    try:
        wishlist = Wishlist.objects.get(wishlist_id = _wishlist_id(request))
        wishlist_items = Wishlist_Item.objects.filter(wishlist=wishlist)
    except ObjectDoesNotExist:
        pass
    context = {
        'total_products' : total_products,
        'wishlist_items' : wishlist_items,
        'userprofile': userprofile,
    }    
    return render(request, 'accounts/dashboard.html', context)

@login_required(login_url='login')
def edit_profile(request):
    userprofile = get_object_or_404(UserProfile, user=request.user)
    if request.method == 'POST':
        user_form = UserForm(request.POST, instance=request.user)
        profile_form = UserProfileForm(request.POST, request.FILES, instance=userprofile)
        if user_form.is_valid() and profile_form.is_valid():
            user_form.save()
            profile_form.save()
            messages.success(request, 'Your profile has been updated.')
            return redirect('edit_profile')
    else:
        user_form = UserForm(instance=request.user)
        profile_form = UserProfileForm(instance=userprofile)
    context = {
        'user_form': user_form,
        'profile_form': profile_form,
        'userprofile': userprofile,
    }
    return render(request, 'accounts/edit_profile.html', context)

@login_required(login_url='login')
def change_password(request):
    if request.method == 'POST':
        current_password = request.POST['current_password']
        new_password = request.POST['new_password']
        confirm_password = request.POST['confirm_password']
        user = Account.objects.get(username__exact=request.user.username)
        if new_password == confirm_password:
            success = user.check_password(current_password)
            if success:
                user.set_password(new_password)
                user.save()
                # auth.logout(request)
                messages.success(request, 'Password updated successfully.')
                return redirect('change_password')
            else:
                messages.error(request, 'Please enter valid current password')
                return redirect('change_password')
        else:
            messages.error(request, 'Password does not match!')
            return redirect('change_password')
    return render(request, 'accounts/change_password.html')

@login_required(login_url='login')
def orders(request):
    orders = Order.objects.filter(user=request.user, is_ordered=True).order_by('-created_at')
    orders_count = orders.count()
    context = {
        'orders_count': orders_count,
        'orders': orders,
        # 'userprofile': userprofile,
    }
    return render(request, 'accounts/orders.html', context)

@login_required(login_url='login')
def order_detail(request, order_id):
    order_detail = OrderProduct.objects.filter(order__order_number=order_id)
    order = Order.objects.get(order_number=order_id)
    context = {
        'order_detail': order_detail,
        'order': order,
    }
    return render(request, 'accounts/order_detail.html', context)


def add_instrument(request):
    if request.method == "POST":
        var1 = request.POST.get('instrumentname')
        var2 = request.POST.get('institute')
        var3 = request.POST.get('category')
        # ins = list(Instrument.objects.filter(Q(instrument_name=var1) & Q(institute = var2)))
        # if len(ins) == 0:
        cat = Category.objects.get(category_name__exact=var3)
        ins = Institute.objects.get(institute_name__exact=var2)
        allInst = Instrument.objects.all()
        inst = Instrument.objects.create()
        inst.slug = slugify(var1) 
        inst.instrument_name = request.POST.get('instrumentname')
        inst.category = cat
        inst.instrument_quantity = request.POST.get('instrumentquantity')
        inst.instrument_description = request.POST.get('instrumentdescription')
        inst.institute = ins
        inst.link = request.POST.get('link')
        inst.instrument_image = request.FILES["file"]
        inst.save()
        messages.success(request, 'Instrument Saved Successfully!')
        # print("A")
        # else:
            # messages.error(request, "Instrument already Exists!")
            # print("AE")
    return render(request,'accounts/add_instrument.html')

def send_status_mail(orderprd, status):
    # prd = get_object_or_404(OrderProduct, order=orderprd)
    order = get_object_or_404(Order, order_number=orderprd.order.order_number)
    fname = order.first_name
    ord_num = order.order_number
    to_email = order.email
    ins = orderprd.instrument
    # print(to_email, fname, ord_num, ins)

    mail_subject = 'Order Status'
    message = render_to_string('accounts/order_status_email.html', {
        'fname': fname,
        'ord_num': ord_num,
        'status': status,
        'ins':ins,
    })
    send_email = EmailMessage(mail_subject, message, to=[to_email])
    send_email.send()   
    return 

@login_required(login_url='login')
def manage_order(request, product=None):
    if request.method == 'GET':
        try:
            new_status = request.GET['dropdown']
        except MultiValueDictKeyError:
            new_status = False
        if new_status:
            prd = get_object_or_404(OrderProduct, id=product)
            prd.status=new_status
            prd.save()
            # print("id",prd.order.order_number)
            # orde = get_object_or_404(Order, order_number=prd.order.order_number)
            # print(orde.order_number)
            # orde.status=new_status 
            # orde.save()
            send_status_mail(prd,new_status)
            # messages.success(request, 'Password reset email has been sent to your email address.')
    instrument_manager = Instrument_Manager.objects.filter(manager=request.user) 
    products = []
    status = []
    products_dict = {}
    for im in instrument_manager:
        nproducts =  OrderProduct.objects.filter(instrument=im.instrument).order_by('-created_at')
        for pr in nproducts:
            orde = get_object_or_404(Order, order_number=pr.order.order_number)
            status.append(orde.status)
            products_dict[pr]=pr.status
            # products_dict[pr]=orde.status 
        products.append(nproducts)
    total_products = len(status)
    context = {
            'products_dict':products_dict,
            'total_products':total_products,
            'products':products,
            'status': status,
            }
    return render(request, 'accounts/manage_order.html', context)



