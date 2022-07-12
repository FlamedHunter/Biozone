from http.client import HTTPResponse
from django.shortcuts import render, redirect, get_object_or_404
from django.core.exceptions import ObjectDoesNotExist
from .models import Instrument, Wishlist, Wishlist_Item
from django.contrib.auth.decorators import login_required
# Create your views here.

def _wishlist_id(request):
    wishlist = request.session.session_key
    if not wishlist:
        wishlist = request.session.create()
    return wishlist


def add_wishlist(request, instrument_id):
    current_user = request.user
    instrument = Instrument.objects.get(id=instrument_id)

    # if current_user.is_authenticated:

    try:
        wishlist = Wishlist.objects.get(wishlist_id=_wishlist_id(request))
    except Wishlist.DoesNotExist:
        wishlist = Wishlist.objects.create(wishlist_id=_wishlist_id(request))
    wishlist.save()

    try:
        wishlist_item = Wishlist_Item.objects.get(instrument=instrument, wishlist=wishlist, user=current_user)
        wishlist_item.save()
    except Wishlist_Item.DoesNotExist:
        wishlist_item = Wishlist_Item.objects.create(
            instrument=instrument,
            wishlist=wishlist,
            user=current_user
        )
        wishlist.save()     
    
    # return HTTPResponse(instrument.instrument_name)
    return redirect('dashboard')

def remove_wishlist(request, instrument_id):
    wishlist = Wishlist.objects.get(wishlist_id=_wishlist_id(request))
    instrument = get_object_or_404(Instrument, id=instrument_id)
    wishlist_item = Wishlist_Item.objects.get(instrument=instrument, wishlist=wishlist)
    wishlist_item.delete()
    return redirect('dashboard') 

def wishlist(request, wishlist_items=None):
    try:
        wishlist = Wishlist.objects.get(wishlist_id = _wishlist_id(request))
        wishlist_items = Wishlist_Item.objects.filter(wishlist=wishlist)
    except ObjectDoesNotExist:
        pass
    context = {
        'wishlist_items' : wishlist_items,
    }    
    return render(request, 'instrument/wishlist.html', context)

@login_required(login_url='login')
def checkout(request, wishlist_items=None):
    try:
        # if request.user.is_authenticated:
            
            # wishlist_items = Wishlist_Item.objects.filter(user=request.user)
        # else:
        wishlist = Wishlist.objects.get(wishlist_id=_wishlist_id(request))
        wishlist_items =  Wishlist_Item.objects.filter(wishlist=wishlist)
    except ObjectDoesNotExist:
        pass

    context = {
        'wishlist_items' : wishlist_items,
    }
    return render(request, 'instrument/checkout.html', context)