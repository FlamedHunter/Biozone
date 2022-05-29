from django.db import models
from django.urls import reverse
# Create your models here.
class Institute(models.Model):
    institute_name = models.CharField(max_length=255, unique=True)
    slug = models.SlugField(max_length=255, unique=True)
    institute_address = models.TextField(max_length=511, blank=True) 
    institute_contact = models.IntegerField()
    institute_email = models.EmailField(max_length=100, unique=True)
    pincode = models.IntegerField()
    institute_image = models.ImageField(upload_to='photos/institute', blank=True)

    def get_url(self):
        return reverse('instruments_by_institute', args=[self.slug])

    def __str__(self):
        return self.institute_name

