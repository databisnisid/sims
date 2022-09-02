from django.contrib import admin
from .models import Notification
from crum import get_current_user
from django import forms
from django.contrib.auth.models import User
from account.models import Account
from django.core.exceptions import ObjectDoesNotExist, ValidationError
from django.utils.translation import gettext as _


class NotificationForm(forms.ModelForm):
    class Meta:
        model = Notification
        fields = '__all__'

    def __init__(self, *args, **kwargs):
        super(NotificationForm, self).__init__(*args, **kwargs)
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
        #print(self.cleaned_data['region'])
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
        else:
            try:
                self.cleaned_data['region']

            except KeyError:
                raise ValidationError(
                    {'region': _('Please assign region!')})


class NotificationAdmin(admin.ModelAdmin):
    form = NotificationForm
    list_display = ['name', 'email']

    class Meta:
        model = Notification

    def get_queryset(self, request):
        user = get_current_user()
        superuser = User.objects.get(username=user)

        if superuser.is_superuser:
            return Notification.objects.all()
        else:
            try:
                account = Account.objects.get(user=user)
                region = account.region
            except ObjectDoesNotExist:
                region = None

            return Notification.objects.filter(region=region)


admin.site.register(Notification, NotificationAdmin)