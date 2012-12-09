from django.conf.urls.defaults import patterns, url, include

from ticketing.api import v1_api
from ticketing.app import application as ticketing_app
from ticketing.dashboard.app import application as ticketing_dashboard_app


urlpatterns = patterns('',
    url(r'^dashboard/support/', include(ticketing_dashboard_app.urls)),
    url(r'^support/', include(ticketing_app.urls)),
    url(r'^api/', include(v1_api.urls)),
)
