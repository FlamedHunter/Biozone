from .models import Wishlist, Wishlist_Item
from .views import _wishlist_id

def counter(request):
    count = 0
    if 'admin' in request.path:
        return {}
    else:
        try:
            wishlist = Wishlist.objects.filter(wishlist_id = _wishlist_id(request))
            wishlist_items = Wishlist_Item.objects.all().filter(wishlist=wishlist[:1])
            for wi in wishlist_items:
                count += 1
        except Wishlist.DoesNotExist:
            count = 0
    return dict(count=count)

