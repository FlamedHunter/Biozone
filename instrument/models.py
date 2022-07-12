from django.db import models
from django.urls import reverse
# from accounts.models import Instrument_Manager

from category.models import Category
from institute.models import Institute
from category.models import Category
# from instrumentmanager.models import Instrument_Manager
# from accounts.models import Account
# from instrument.current_user import get_current_user
# Create your models here.

class Instrument(models.Model):
    instrument_name = models.CharField(max_length=200)
    slug = models.SlugField(max_length=200)
    instrument_description = models.TextField(max_length=500, blank=True)
    instrument_quantity = models.IntegerField()
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    institute = models.ForeignKey(Institute, on_delete=models.CASCADE)
    instrument_image = models.ImageField(upload_to='photos/instrument', blank=True)
    link = models.CharField(max_length=100, blank=True)
    # added_by = models.ForeignKey("accounts.Account", null=True, blank=True, on_delete=models.SET_NULL)

    def get_url(self):
        return reverse('instrument_detail', args=[self.category.slug, self.slug])

    def __str__(self):
        return self.instrument_name

    # def save(self, *args, **kwargs):
    #     is_new = True if not self.id else False
    #     super(Instrument, self).save(*args, **kwargs)
    #     if is_new:
    #         im = Instrument_Manager(Instrument=self)
    #         im.save()
    

