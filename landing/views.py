from django.shortcuts import render
from location.models import Location
from django.conf import settings


def index(request):
    location = Location.objects.all()

    return render(request, 'index.html', {
        'location': location,
        'settings': settings,
    })
