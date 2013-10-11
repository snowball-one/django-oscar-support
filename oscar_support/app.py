from django.conf.urls.defaults import patterns, url
from django.contrib.auth.decorators import login_required

from oscar.core.application import Application

from . import views


class SupportApplication(Application):
    name = 'support'

    ticket_list_view = views.TicketListView
    ticket_create_view = views.TicketCreateView
    ticket_update_view = views.TicketUpdateView

    def get_urls(self):
        urlpatterns = super(SupportApplication, self).get_urls()

        urlpatterns += patterns('',
            url(
                r'accounts/support/$',
                self.ticket_list_view.as_view(),
                name='customer-ticket-list'
            ),
            url(
                r'accounts/support/ticket/create/$',
                self.ticket_create_view.as_view(),
                name='customer-ticket-create'
            ),
            url(
                r'accounts/support/ticket/(?P<pk>\d+)/update/$',
                self.ticket_update_view.as_view(),
                name='customer-ticket-update'
            ),
        )
        return self.post_process_urls(urlpatterns)

    def get_url_decorator(self, url_name):
        return login_required


application = SupportApplication()
