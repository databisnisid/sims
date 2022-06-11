from django.db import models
from django.contrib.auth.models import User
from django.utils.translation import gettext as _


class Region(models.Model):
    name = models.CharField(_('Region Name'), max_length=50)
    code = models.CharField(_('Region Code'), max_length=20, unique=True)
    map_center = models.CharField(_('Map Center'), max_length=100,
                                  default='-1.233982000061532, 116.83728437200422')
    map_zoom = models.IntegerField(_('Map Zoom'), default=9)

    created_at = models.DateTimeField(auto_now=False, auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True, auto_now_add=False)

    class Meta:
        db_table = 'region'
        verbose_name = _('region')
        verbose_name_plural = _('region list')

    def __str__(self):
        return '%s' % self.name

    def save(self):
        self.name = self.name.upper()
        self.code = self.code.upper()
        return super(Region, self).save()


class Account(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    region = models.ForeignKey(
        Region,
        on_delete=models.RESTRICT,
        verbose_name=_('Region')
    )

    class Meta:
        db_table = 'account'
        verbose_name = _('account')
        verbose_name_plural = _('account list')

    created_at = models.DateTimeField(auto_now=False, auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True, auto_now_add=False)

    def __str__(self):
        return '%s' % self.user

