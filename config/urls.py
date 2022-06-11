from django.contrib import admin
from django.urls import path, include
from landing.views import index
from django.utils.translation import gettext as _

admin.site.site_header = _('Surveillance Integration Monitoring System')

urlpatterns = [
    path('', index, name='index'),
    path('grappelli/', include('grappelli.urls')), # grappelli URLS
    path('login/', admin.site.urls),
]
