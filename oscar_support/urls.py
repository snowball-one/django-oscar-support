from django.conf.urls.defaults import patterns, url, include

from .api import v1_api
from .app import application as oscar_support_app
from .dashboard.app import application as oscar_support_dashboard_app


urlpatterns = patterns(
    '',
    url(r'^dashboard/support/', include(oscar_support_dashboard_app.urls)),
    url(r'^', include(oscar_support_app.urls)),
    url(r'^api/', include(v1_api.urls)),
)
