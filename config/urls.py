from django.contrib import admin
from django.urls import path, include
from landing.views import index, index_json, frontend_view
from django.utils.translation import gettext as _
from django.conf import settings

admin.site.site_header = _("Surveillance Integration Monitoring System")

urlpatterns = [
    path("", index, name="index"),
    path("json/", index_json, name="index_json"),
    path("frontend/", frontend_view, name="front_end"),
    path("grappelli/", include("grappelli.urls")),  # grappelli URLS
    path("login/", admin.site.urls),
]

if settings.DEBUG:
    from django.conf.urls.static import static
    from django.contrib.staticfiles.urls import staticfiles_urlpatterns

    # Serve static and media files from development server
    urlpatterns += staticfiles_urlpatterns()
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
