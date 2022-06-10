from django.contrib import admin
from django.urls import path, include
from landing.views import index


urlpatterns = [
    path('', index, name='index'),
    path('grappelli/', include('grappelli.urls')), # grappelli URLS
    path('login/', admin.site.urls),
]
