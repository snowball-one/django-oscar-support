from django.http import Http404
from django.db.models import get_model, Q
from tastypie.utils import trailing_slash
from django.conf.urls.defaults import url
from django.contrib.sites.models import Site
from django.template import Template, RequestContext
from django.core.paginator import Paginator, InvalidPage

from tastypie import fields
from tastypie.api import Api
from tastypie.constants import ALL, ALL_WITH_RELATIONS
from tastypie.resources import ModelResource
from tastypie.authorization import ReadOnlyAuthorization

from ticketing.api.authentication import SessionAuthentication

v1_api = Api(api_name='v1')


Ticket = get_model('ticketing', 'Ticket')


class SearchableModelResource(ModelResource):

    def get_search(self, request, **kwargs):
        queryset = self.get_object_list(request)
        return self.get_search_in_queryset(queryset, request, **kwargs)

    def get_search_in_queryset(self, queryset, request, **kwargs):
        self.method_check(request, allowed=['get'])
        self.is_authenticated(request)
        self.throttle_check(request)

        queryset = self.get_filtered_queryset(
            queryset,
            request.GET.get('q', '')
        )

        paginator = Paginator(queryset, 20)

        try:
            page = paginator.page(int(request.GET.get('page', 1)))
        except InvalidPage:
            raise Http404("Sorry, no results on that page.")

        objects = []

        for result in page.object_list:
            bundle = self.build_bundle(obj=result, request=request)
            bundle = self.full_dehydrate(bundle)
            objects.append(bundle)

        object_list = {
            'objects': objects,
        }

        self.log_throttled_access(request)
        return self.create_response(request, object_list)



class CommunicationEventTypeResource(ModelResource):
    class Meta:
        queryset = get_model('customer', 'CommunicationEventType').objects.all()
        resource_name = 'communicationeventtype'
        authorization = ReadOnlyAuthorization()
        authentication = SessionAuthentication()

    def dehydrate(self, bundle):
        ticket_id = bundle.request.GET.get('ticket_id', None)
        try:
            ticket = Ticket.objects.get(id=ticket_id)
        except Ticket.DoesNotExist:
            del bundle.data['email_body_html_template']
            del bundle.data['email_body_template']
            del bundle.data['email_subject_template']
            return bundle

        ctx = {
            'ticket': ticket,
            'user': ticket.requester,
            'site': Site.objects.get_current(),
        }

        if ticket.relatedorders.count():
            # FIXME: what should we do here to make it better?
            ctx['order'] = ticket.relatedorders.all()[0].order

        if ticket.relatedlines.count():
            ctx['line_list'] = ticket.relatedlines.all()

        if ticket.relatedproducts.count():
            ctx['product_list'] = ticket.relatedproducts.all()

        ctx = RequestContext(bundle.request, ctx)

        tmpl = Template(bundle.data['email_body_html_template'])
        bundle.data['email_body_html_template'] = tmpl.render(ctx)

        tmpl = Template(bundle.data['email_body_template'])
        bundle.data['email_body_template'] = tmpl.render(ctx)

        tmpl = Template(bundle.data['email_subject_template'])
        bundle.data['email_subject_template'] = tmpl.render(ctx)
        return bundle


class UserResource(SearchableModelResource):
    class Meta:
        queryset = get_model('auth', 'User').objects.all()
        resource_name = 'user'
        authorization = ReadOnlyAuthorization()
        authentication = SessionAuthentication()
        fields = ['username', 'email', 'first_name', 'last_name', 'id']

    def override_urls(self):
        return [
            url(r"^agent/search%s$" % (
                trailing_slash()),
                self.wrap_view('get_agent_search'),
                name="api_get_agent_search"
            ),
            url(r"^(?P<resource_name>%s)/search%s$" % (
                self._meta.resource_name,
                trailing_slash()),
                self.wrap_view('get_search'),
                name="api_get_search"
            )
        ]

    def dehydrate(self, bundle):
        first_name = bundle.data['first_name']
        last_name = bundle.data['last_name']
        if first_name or last_name:
            bundle.data['label'] = "%s %s" % (first_name, last_name)
        else:
            bundle.data['label'] = bundle.data['email']
        bundle.data['value'] = bundle.data['id']
        return bundle

    def get_agent_search(self, request, **kwargs):
        queryset = self.get_object_list(request).filter(is_staff=True)
        return self.get_search_in_queryset(queryset, request, **kwargs)

    def get_filtered_queryset(self, queryset, search_term):
        fn_search = search_term
        ln_search = fn_search

        if len(fn_search.split(' ')) == 2:
            fn_search, ln_search = fn_search.split(' ')

        return queryset.filter(
            Q(email__icontains=fn_search) |
            Q(first_name__icontains=fn_search) |
            Q(last_name__icontains=ln_search)
        )


class OrderResource(ModelResource):
    user = fields.ForeignKey(UserResource, 'user')

    class Meta:
        queryset = get_model('order', 'Order').objects.all()
        resource_name = 'order'
        authorization = ReadOnlyAuthorization()
        authentication = SessionAuthentication()


class GroupResource(SearchableModelResource):
    class Meta:
        queryset = get_model('auth', 'Group').objects.all()
        resource_name = 'group'
        authorization = ReadOnlyAuthorization()
        authentication = SessionAuthentication()

    def dehydrate(self, bundle):
        bundle.data['label'] = bundle.data['name']
        bundle.data['value'] = bundle.data['id']
        return bundle

    def override_urls(self):
        return [
            url(r"^(?P<resource_name>%s)/search%s$" % (
                self._meta.resource_name,
                trailing_slash()),
                self.wrap_view('get_search'),
                name="api_get_search"
            )
        ]

    def get_filtered_queryset(self, queryset, search_term):
        return queryset.filter(name__icontains=search_term)


v1_api.register(CommunicationEventTypeResource())
v1_api.register(UserResource())
v1_api.register(OrderResource())
v1_api.register(GroupResource())
