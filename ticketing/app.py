from django.conf.urls.defaults import include, patterns, url

from oscar.core.application import Application

from ticketing.api import v1_api


class TicketingApplication(Application):
    name = 'ticketing'

    def get_urls(self):
        urlpatterns = super(TicketingApplication, self).get_urls()

        urlpatterns += patterns('',
            url(r'^api/', include(v1_api.urls)),
        )
        return self.post_process_urls(urlpatterns)


application = TicketingApplication()
