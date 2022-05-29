from django.contrib import admin
from .models import Wishlist, Wishlist_Item
# Register your models here.

admin.site.register(Wishlist)
admin.site.register(Wishlist_Item)