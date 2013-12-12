from django.conf.urls import patterns, url

from shortuuid import get_alphabet

from oscar.core.application import Application
from oscar.views.decorators import staff_member_required

from . import views


class SupportDashboardApplication(Application):
    name = 'support-dashboard'

    ticket_list_view = views.TicketListView
    ticket_create_view = views.TicketCreateView
    ticket_update_view = views.TicketUpdateView

    def get_urls(self):
        urlpatterns = patterns(
            '',
            url(r'^$', self.ticket_list_view.as_view(), name='ticket-list'),
            url(r'^ticket/create/$', self.ticket_create_view.as_view(),
                name='ticket-create'),
            url(
                r'^ticket/update/(?P<pk>[{0}]+)/$'.format(get_alphabet()),
                self.ticket_update_view.as_view(),
                name='ticket-update'
            ),
        )
        return self.post_process_urls(urlpatterns)

    def get_url_decorator(self, url_name):
        return staff_member_required


application = SupportDashboardApplication()
