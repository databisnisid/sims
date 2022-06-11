from django.shortcuts import render
from location.models import Location
from account.models import Region
from django.conf import settings
from django.views.generic import ListView
from django.db.models import Q
from django.core.exceptions import ObjectDoesNotExist


def index(request):
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

    return render(request, 'index.html', {
        'location': location,
        'region': region,
        'specific_region': specific_region,
        'settings': settings,
    })


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
