from django.contrib import admin
from .models import Account, Region


class AccountAdmin(admin.ModelAdmin):
    list_display = ['user', 'region']

    class Meta:
        model = Account


class RegionAdmin(admin.ModelAdmin):
    list_display = ['name', 'code']

    class Meta:
        model = Region


admin.site.register(Account, AccountAdmin)
admin.site.register(Region, RegionAdmin)
