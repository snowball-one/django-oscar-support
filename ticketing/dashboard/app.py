from django.conf.urls.defaults import patterns, url
from django.utils.translation import ugettext_lazy as _

from oscar.core.application import Application
from oscar.apps.dashboard.nav import register, Node
from oscar.views.decorators import staff_member_required

from ticketing.dashboard import views


node = Node(_('Support'))
node.add_child(Node(_('Overview'), 'ticketing-dashboard:ticket-list'))
register(node, 180)


class TicketingDashboardApplication(Application):
    name = 'ticketing-dashboard'

    ticket_list_view = views.TicketListView
    ticket_create_view = views.TicketCreateView
    ticket_update_view = views.TicketUpdateView

    def get_urls(self):
        urlpatterns = patterns('',
            url(r'^$', self.ticket_list_view.as_view(), name='ticket-list'),
            url(r'^ticket/create/$', self.ticket_create_view.as_view(),
                name='ticket-create'),
            url(r'^ticket/update/(?P<pk>\d+)/$', self.ticket_update_view.as_view(),
                name='ticket-update'),
        )
        return self.post_process_urls(urlpatterns)

    def get_url_decorator(self, url_name):
        return staff_member_required

application = TicketingDashboardApplication()
