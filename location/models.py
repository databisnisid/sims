from django.db import models
from django_google_maps import fields as map_fields
from connector.models import Device
from account.models import Account, Region
from django.utils.translation import gettext as _
from crum import get_current_user
from django.core.exceptions import ObjectDoesNotExist


CHANNEL_STATUS = [
    ('DISABLE', -1),
    ('OK', 1),
    ('PROBLEM', 0),
]


class Location(models.Model):
    name = models.CharField(max_length=100, unique=True, verbose_name='Location')
    region = models.ForeignKey(
        Region,
        on_delete=models.RESTRICT,
        verbose_name=_('Region')
    )
    address = map_fields.AddressField(max_length=200, blank=True, verbose_name='Address')
    geolocation = map_fields.GeoLocationField(max_length=100, blank=True)

    # Technical
    ipaddress = models.GenericIPAddressField(verbose_name='IP Address')
    port = models.IntegerField(default=161, verbose_name=_('Port'))
    device = models.ForeignKey(
        Device,
        on_delete=models.RESTRICT,
        verbose_name=_('Device'),
        null=True,
        blank=True
    )
    #
    parameter_1 = models.BooleanField(default=False, verbose_name=_('Parameter 1'))
    parameter_2 = models.BooleanField(default=False, verbose_name=_('Parameter 2'))
    parameter_3 = models.BooleanField(default=False, verbose_name=_('Parameter 3'))
    parameter_4 = models.BooleanField(default=False, verbose_name=_('Parameter 4'))
    status_1 = models.IntegerField(default=-1, verbose_name=_('Status 1'))
    status_2 = models.IntegerField(default=-1, verbose_name=_('Status 2'))
    status_3 = models.IntegerField(default=-1, verbose_name=_('Status 3'))
    status_4 = models.IntegerField(default=-1, verbose_name=_('Status 4'))

    ping_status = models.BooleanField(default=True, verbose_name=_('Ping Status'))

    created_at = models.DateTimeField(auto_now=False, auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True, auto_now_add=False)

    class Meta:
        db_table = 'location'
        verbose_name = 'location'
        verbose_name_plural = 'Location List'

    def __str__(self):
        return '%s' % self.name
    
    def save(self):
        self.name = self.name.upper()

        if self.device is None:
            self.parameter_1 = False
            self.parameter_2 = False
            self.parameter_3 = False
            self.parameter_4 = False

        if not self.parameter_1:
            self.status_1 = -1

        if not self.parameter_2:
            self.status_2 = -1

        if not self.parameter_3:
            self.status_3 = -1

        if not self.parameter_4:
            self.status_4 = -1

        user = get_current_user()
        try:
            account = Account.objects.get(user=user)
            if account.region is not None:
                self.region = account.region
        except ObjectDoesNotExist:
            pass

        return super(Location, self).save()


        