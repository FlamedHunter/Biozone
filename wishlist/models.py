from django.db import models
from instrument.models import Instrument
from accounts.models import Account
# Create your models here.
class Wishlist(models.Model):
    wishlist_id = models.CharField(max_length=500, blank=True)
    date_added = models.DateField(auto_now_add=True)
    
    def __str__(self):
        return self.wishlist_id

class Wishlist_Item(models.Model):
    user = models.ForeignKey(Account, on_delete=models.CASCADE, null=True)
    instrument = models.ForeignKey(Instrument, on_delete=models.CASCADE)
    wishlist = models.ForeignKey(Wishlist, on_delete=models.CASCADE, null=True)
    is_active = models.BooleanField(default=True)

    def __unicode__(self):
        return self.instrument