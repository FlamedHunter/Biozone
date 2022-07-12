from django.shortcuts import render
from instrument.models import Instrument
from django.core.mail import EmailMessage

def home(request):
    instruments = Instrument.objects.all()
    context = {
        'instruments' : instruments,
    }
    return render(request, 'home.html', context)

def team(request):
    return render(request,'team.html', {})