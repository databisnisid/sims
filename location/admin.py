from django.contrib import admin
from .models import Location
from account.models import Account
from django_google_maps import widgets as map_widgets
from django_google_maps import fields as map_fields
from django import forms
from django.utils.translation import gettext as _
from crum import get_current_user
from django.core.exceptions import ObjectDoesNotExist, ValidationError


class LocationForm(forms.ModelForm):

    class Meta:
        model = Location
        fields = '__all__'

    def clean(self):
        #po_number = self.cleaned_data['region']
        #project = self.cleaned_data['project']
        user = get_current_user()
        #print(user)
        try:
            account = Account.objects.get(user=user)
            #if account.region is None:
            #    raise ValidationError(_('No Region is assigned to User. Please assign region to user in Account'))
        except ObjectDoesNotExist:
            raise ValidationError(_('No Region is assigned to User. Please assign region to user in Account'))


class LocationAdmin(admin.ModelAdmin):
    form = LocationForm
    formfield_overrides = {
        map_fields.AddressField: {
          'widget': map_widgets.GoogleMapsAddressWidget(attrs={
              'data-map-type': 'roadmap',
              'placeholder': 'Masukkan alamat dan tekan enter',
              'size': 200
          })
        },
        map_fields.GeoLocationField: {
            'widget': forms.TextInput(attrs={
                'readonly': 'readonly',
            })
        },
    }

    fieldsets = (
        (_('Location Detail'), {
            'classes': ('grp-collapse grp-open',),
            'fields': (
                'region', 'name', 'address', 'geolocation',
            )
        }),
        (_('Technical'), {
            'classes': ('grp-collapse grp-closed',),
            'fields': (
                ('ipaddress', 'port'), 'device',
                ('parameter_1', 'parameter_2', 'parameter_3', 'parameter_4')
            )
        }),
    )

    list_display = ['name', 'address', 'geolocation',
                    'ipaddress', 'device',
                    'parameter_1', 'parameter_2', 'parameter_3', 'parameter_4',
                    'region']
    exclude = ['created_at', 'updated_at']
    readonly_fields = ['region']

    class Meta:
        model = Location

    def get_queryset(self, request):
        user = get_current_user()

        try:
            account = Account.objects.get(user=user)
            region = account.region
        except ObjectDoesNotExist:
            region = None

        return Location.objects.filter(region=region)

'''
class StackedItemInline(admin.StackedInline):
    classes = ('grp-collapse grp-open',)


class TabularItemInline(admin.TabularInline):
    classes = ('grp-collapse grp-open',)
'''

admin.site.register(Location, LocationAdmin)
