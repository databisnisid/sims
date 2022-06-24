import os
from django.contrib import admin
from .models import Location
from account.models import Account
from django_google_maps import widgets as map_widgets
from django_google_maps import fields as map_fields
from django import forms
from django.utils.translation import gettext as _
from crum import get_current_user
from django.core.exceptions import ObjectDoesNotExist, ValidationError
from django.contrib.auth.models import User
from django.utils.html import format_html
from connector.utils import update_parameter_status_per_loc
from django.conf import settings


class LocationForm(forms.ModelForm):

    class Meta:
        model = Location
        fields = '__all__'

    def __init__(self, *args, **kwargs):
        super(LocationForm, self).__init__(*args, **kwargs)
        user = get_current_user()
        superuser = User.objects.get(username=user)
        print(user)
        print(superuser.is_superuser)
        if superuser.is_superuser:
            self.fields['region'].disabled = False
        else:
            self.fields['region'].disabled = True
            self.fields['region'].required = False
            #self.fields['region'].widget.attrs['readonly'] = 'readonly'

    def clean(self):
        #region = self.cleaned_data['region']
        #project = self.cleaned_data['project']
        print(self.cleaned_data['region'])
        user = get_current_user()
        superuser = User.objects.get(username=user)
        #print(user)
        #print(superuser.is_superuser)
        if superuser.is_superuser is not True:
            try:
                account = Account.objects.get(user=user)
                if account.region is None:
                    raise ValidationError({'region': _('Please assign region to user')})
                #    print(account.region)
                #    self.cleaned_data['region'] = account.region
                #    print(self.cleaned_data['region'])
                #    raise ValidationError({'region': _('Please assign region')})
            except ObjectDoesNotExist:
                raise ValidationError(_('No Region is assigned to User. Please assign region to user in Account'))


def status_string(value, channel, ipaddress):
    """ Convert integer value status to meaningful STRING """

    if value == 0:
        status = 'DOWN'
    elif value == 1:
        status = 'OK'
    else:
        status = 'DISABLE'
    user = get_current_user()
    superuser = User.objects.get(username=user)
    media_path = settings.MEDIA_ROOT + '/camera'
    image_path = media_path + '/' + ipaddress + '_' + str(channel) + '.png'
    if superuser.is_superuser and os.path.exists(image_path):
        #pass
        result = '<a href="' + settings.MEDIA_URL + '/camera/'
        result += ipaddress + '_' + str(channel) + '.png" target="_blank">'
        result += status
        result += '</a>'
        status = result

    return format_html(status)


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
            )
        }),
    )

    list_display = ['name', 'address', 'geolocation',
                    'ipaddress', 'device', 'device_type',
                    'ping_status',
                    'camera_1', 'camera_2', 'camera_3', 'camera_4',
                    'region']

    #list_display_links = ['snapshot_1']

    exclude = ['created_at', 'updated_at']
    readonly_fields = ['device_type']
    actions = ['update_parameter_status']
    change_list_template = 'admin/change_list.html'

    class Meta:
        model = Location

    def changelist_view(self, request, extra_context=None):
        if not request.user.is_superuser:
            self.list_display = ['name', 'address', 'geolocation',
                                 'ipaddress', 'device',
                                 'camera_1', 'camera_2', 'camera_3', 'camera_4',
                                 'region']
        else:
            self.list_display = ['name', 'address', 'geolocation',
                                 'ipaddress', 'device', 'device_type', 'ping_status',
                                 'camera_1', 'camera_2', 'camera_3', 'camera_4',
                                 'region']

        return super(LocationAdmin, self).changelist_view(request, extra_context)

    def get_queryset(self, request):
        user = get_current_user()
        superuser = User.objects.get(username=user)

        if superuser.is_superuser:
            return Location.objects.all()
        else:
            try:
                account = Account.objects.get(user=user)
                region = account.region
            except ObjectDoesNotExist:
                region = None

            return Location.objects.filter(region=region)

    def update_parameter_status(self, request, queryset):
        for obj in queryset:
            update_parameter_status_per_loc(obj)

    update_parameter_status.short_description = 'Check Camera Status'

    def image_tag(self, obj):
        return format_html('<img src="lsajdla" />')

    image_tag.short_description = 'Image'

    @staticmethod
    def camera_1(obj):
        return status_string(obj.status_1, 1, obj.ipaddress)
    camera_1.allow_tags = True

    @staticmethod
    def camera_2(obj):
        return status_string(obj.status_2, 2, obj.ipaddress)
    camera_2.allow_tags = True

    @staticmethod
    def camera_3(obj):
        return status_string(obj.status_3, 3, obj.ipaddress)
    camera_3.allow_tags = True

    @staticmethod
    def camera_4(obj):
        return status_string(obj.status_4, 4, obj.ipaddress)
    camera_4.allow_tags = True


'''
class StackedItemInline(admin.StackedInline):
    classes = ('grp-collapse grp-open',)


class TabularItemInline(admin.TabularInline):
    classes = ('grp-collapse grp-open',)
'''

admin.site.register(Location, LocationAdmin)
