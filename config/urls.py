from django.contrib import admin
from django.urls import path, include
from landing.views import index, index_json, frontend_view
from django.utils.translation import gettext as _

admin.site.site_header = _('Surveillance Integration Monitoring System')

urlpatterns = [
    path('', index, name='index'),
    path('json/', index_json, name='index_json'),
    path('frontend/', frontend_view, name='front_end'),
    path('grappelli/', include('grappelli.urls')), # grappelli URLS
    path('login/', admin.site.urls),
]
