from django.conf import settings
from django.contrib import admin
from django.conf.urls.static import static
from django.conf.urls import patterns, include, url
from django.contrib.staticfiles.urls import staticfiles_urlpatterns

from oscar.app import shop
from ticketing.app import application as ticketing_app
from ticketing.dashboard.app import application as ticketing_dashboard_app

admin.autodiscover()

urlpatterns = patterns('',
    url(r'^', include(shop.urls)),

    url(r'^dashboard/support/', include(ticketing_dashboard_app.urls)),
    url(r'^support/', include(ticketing_app.urls)),

    url(r'^admin/', include(admin.site.urls)),
)


if settings.DEBUG:
    urlpatterns += staticfiles_urlpatterns()
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
