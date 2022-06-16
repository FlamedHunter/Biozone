from django.db import models
from django.urls import reverse

from category.models import Category
from institute.models import Institute
from category.models import Category

# Create your models here.
class Instrument(models.Model):
    # instrument_id = models.CharField(primary_key=True, max_length=10)
    instrument_name = models.CharField(max_length=200)
    slug = models.SlugField(max_length=200)
    instrument_description = models.TextField(max_length=500, blank=True)
    instrument_quantity = models.IntegerField()
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    institute = models.ForeignKey(Institute, on_delete=models.CASCADE)
    instrument_image = models.ImageField(upload_to='photos/instrument', blank=True)
    link = models.CharField(max_length=100, blank=True)

    def get_url(self):
        return reverse('instrument_detail', args=[self.category.slug, self.slug])

    def __str__(self):
        return self.instrument_name

