import json
from django.shortcuts import render
from location.models import Location
from account.models import Region
from django.conf import settings
from django.views.generic import ListView
from django.db.models import Q
from django.core.exceptions import ObjectDoesNotExist
from django.http import JsonResponse
from django.core import serializers
from django.views.decorators.csrf import csrf_exempt


def index(request):
    query = request.GET.get('q')
    region = None
    specific_region = None
    #print(query)

    if query is not None:
        try:
            specific_region = Region.objects.get(code=query)

        except ObjectDoesNotExist:
            pass

    if specific_region:
        location = Location.objects.filter(
            Q(region=specific_region)
        )
    else:
        location = Location.objects.all()

    region = Region.objects.all()

    return render(request, 'index.html', {
        'location': location,
        'region': region,
        'specific_region': specific_region,
        'settings': settings,
    })


'''
class LocationSerializer(serializers.):

    class Meta:
        model = Location
        fields = '__all__'
'''


@csrf_exempt
def index_json(request):
    query = request.GET.get('q')
    region = None
    specific_region = None
    print(query)

    if query is not None:
        try:
            specific_region = Region.objects.get(code=query)

        except ObjectDoesNotExist:
            pass

    if specific_region:
        location = Location.objects.filter(
            Q(region=specific_region)
        )
    else:
        location = Location.objects.all()

    region = Region.objects.all()

    print(region)
    location = serializers.serialize('json', location)
    region = serializers.serialize('json', region)

    print(specific_region)

    if specific_region is not None:
        specific_region = {
            'status': 'true',
            'code': specific_region.code,
        }
    else:
        specific_region = {
            'status': 'false',
            'code': '',
        }

    google_map = {
        'MAPS_KEY': settings.GOOGLE_MAPS_API_KEY,
        'MAPS_CENTER': settings.MAPS_CENTER_PLAIN,
        'MAPS_ZOOM': settings.MAPS_ZOOM
    }

    data = {
        'location': json.loads(location),
        'region': json.loads(region),
        'specific_region': specific_region,
        'google_map': google_map,
    }

    return JsonResponse(data)


def frontend_view(request):
    # render function takes argument  - request
    # and return HTML as response
    return render(request, "frontend.html")


class IndexView(ListView):
    model = Location
    template_name = 'landing/index.html'

    # queryset = Anggota.objects.filter(name__icontains='Dedy') # new

    def get_queryset(self):  # new
        query = self.request.GET.get('q')
        if query:
            location = ListView.objects.filter(
                Q(region=query)
            )

        else:
            location = ListView.objects.all()

        return location
