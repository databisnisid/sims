from django.contrib import admin
from .models import Device, Parameter


class ParameterAdmin(admin.ModelAdmin):
    list_display = ['name', 'connector', 'value']

    class Meta:
        model = Parameter


class DeviceAdmin(admin.ModelAdmin):
    list_display = ['name', 'connector', 'parameter_type',
                    'parameter_1', 'parameter_2', 'parameter_3', 'parameter_4']

    class Meta:
        model = Device


admin.site.register(Parameter, ParameterAdmin)
admin.site.register(Device, DeviceAdmin)
