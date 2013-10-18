from django.conf import settings
from django.conf.urls.defaults import url, patterns, include

from rest_framework import routers

from . import views


router = routers.DefaultRouter()
router.register(r'customers', views.CustomerViewSet, base_name="customer")
router.register(r'agents', views.AgentViewSet, base_name="agent")
router.register(r'groups', views.GroupViewSet)


urlpatterns = patterns(
    '',
    url(r'^', include(router.urls, namespace='support-api')),
)


if settings.DEBUG:
    urlpatterns = urlpatterns + patterns(
        '',
        url(
            r'^api-auth/',
            include('rest_framework.urls', namespace='rest_framework')
        ),
    )
