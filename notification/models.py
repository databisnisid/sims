from django.db import models
from crum import get_current_user
from django.core.exceptions import ObjectDoesNotExist
from account.models import Account, Region
from django.utils.translation import gettext as _


class Notification(models.Model):
    name = models.CharField(max_length=50, verbose_name=_('Name'))
    email = models.EmailField()
    region = models.ForeignKey(
        Region,
        on_delete=models.RESTRICT,
        verbose_name=_('Region')
    )

    created_at = models.DateTimeField(auto_now=False, auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True, auto_now_add=False)

    class Meta:
        db_table = 'notification'
        verbose_name = 'notification'
        verbose_name_plural = 'notifications'

    def __str__(self):
        return '%s' % self.name

    def save(self):
        self.name = self.name.upper()

        user = get_current_user()
        try:
            account = Account.objects.get(user=user)
            if account.region is not None:
                self.region = account.region
        except ObjectDoesNotExist:
            pass

        return super(Notification, self).save()