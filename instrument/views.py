from django.http import HttpResponse
from django.shortcuts import render, get_object_or_404
from django.core.paginator import EmptyPage, Paginator, PageNotAnInteger
from category.models import Category
from institute.models import Institute
from wishlist.models import Wishlist_Item
from wishlist.views import _wishlist_id
from instrument.models import Instrument
from django.db.models import Q
# Create your views here.
def instrument(request, category_slug=None, institute_slug=None):
    categories = None
    institutes = None
    instruments = None
    # if institute_slug != None and category_slug != None:
    #     institutes = get_object_or_404(Institute, slug=institute_slug)
    #     categories = get_object_or_404(Category, slug=category_slug)
    #     instruments = Instrument.objects.filter(institute = institutes, category = categories)    
    #     paginator = Paginator(instruments, 6)
    #     page = request.GET.get('page')
    #     paged_instruments = paginator.get_page(page)
    #     instruments_count = instruments.count()

    # elif institute_slug != None:
    #     institutes = get_object_or_404(Institute, slug=institute_slug)
    #     instruments = Instrument.objects.filter(institute = institutes).order_by('id')
    #     paginator = Paginator(instruments, 6)
    #     page = request.GET.get('page')
    #     paged_instruments = paginator.get_page(page)  
    #     instruments_count = instruments.count()

    if category_slug != None:
        categories = get_object_or_404(Category, slug=category_slug)
        instruments = Instrument.objects.filter(category = categories)    
        paginator = Paginator(instruments, 6)
        page = request.GET.get('page')
        paged_instruments = paginator.get_page(page)
        instruments_count = instruments.count()
    elif institute_slug != None:
        institutes = get_object_or_404(Institute, slug=institute_slug)
        instruments = Instrument.objects.filter(institute = institutes)    
        paginator = Paginator(instruments, 6)
        page = request.GET.get('page')
        paged_instruments = paginator.get_page(page)
        instruments_count = instruments.count()
    else:
        instruments = Instrument.objects.all()
        paginator = Paginator(instruments, 6)
        page = request.GET.get('page')
        paged_instruments = paginator.get_page(page)
        instruments_count = instruments.count()

    context = {
        'instruments' : paged_instruments,
        'instruments_count' : instruments_count,
    }
    return render(request, 'instrument/instrument.html', context)

def instrument_detail(request, category_slug, instrument_slug):
    try:
        req_instrument = Instrument.objects.get(category__slug=category_slug, slug=instrument_slug)
        in_wishlist = Wishlist_Item.objects.filter(wishlist__wishlist_id=_wishlist_id(request), instrument=req_instrument).exists()
    except Exception as e:
        raise e
    context = {
        'req_instrument': req_instrument,
        'in_wishlist' :in_wishlist,
    }
    return render(request, 'instrument/instrument_detail.html', context) 


def search(request):
    # return HttpResponse('searchpage')
    if 'keyword' in request.GET:
        keyword = request.GET['keyword']
        if keyword:
            instruments = Instrument.objects.order_by('instrument_name').filter(Q(instrument_name__icontains=keyword) | Q(instrument_description__icontains=keyword))
            instruments_count = instruments.count()
        else:
            instruments_count = 0
            instruments = None
    context = {
        'instruments_count' : instruments_count,
        'instruments':instruments,
    }
    return render(request, 'instrument/instrument.html', context)
