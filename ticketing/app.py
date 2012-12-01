from django.conf.urls.defaults import patterns, url

from oscar.core.application import Application

#from ticketing import views


class TicketingApplication(Application):
    name = 'ticketing'
    #list_view = views.StoreListView
    #detail_view = views.StoreDetailView

    def get_urls(self):
        urlpatterns = super(TicketingApplication, self).get_urls()

        urlpatterns += patterns('',
            #url(r'^$', self.list_view.as_view(), name='index'),
            #url(r'^(?P<slug>[\w-]+)/$', self.detail_view.as_view(), name='detail'),
        )
        return self.post_process_urls(urlpatterns)


application = TicketingApplication()
