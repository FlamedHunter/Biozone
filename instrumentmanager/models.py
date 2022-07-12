from django.db import models
from instrument.models import Instrument
from accounts.models import Account
# Create your models here.


class Instrument_Manager(models.Model):
    manager = models.ForeignKey(Account, on_delete=models.CASCADE)
    instrument = models.ForeignKey(Instrument, on_delete=models.CASCADE)
    def __str__(self):
        return self.instrument.instrument_name


