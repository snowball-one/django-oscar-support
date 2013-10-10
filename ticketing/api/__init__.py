from django.http import Http404
from django.db import IntegrityError
from django.db.models import get_model, Q
from django.conf.urls.defaults import url
from django.contrib.sites.models import Site
from django.template import Template, RequestContext
from django.utils.translation import ugettext_lazy as _
from django.core.paginator import Paginator, InvalidPage

from sorl.thumbnail import get_thumbnail

from oscar.templatetags.currency_filters import render_currency

from tastypie.api import Api
from tastypie.utils import trailing_slash
from tastypie.exceptions import BadRequest
from tastypie.resources import ModelResource
from tastypie.validation import FormValidation
from tastypie.authorization import (ReadOnlyAuthorization,
                                    DjangoAuthorization)

from oscar.apps.customer.forms import generate_username

from ticketing.dashboard.forms import RequesterCreateForm
from ticketing.api.authentication import SessionAuthentication

User = get_model('auth', 'User')
Ticket = get_model('ticketing', 'Ticket')


v1_api = Api(api_name='v1')


class SearchableModelResource(ModelResource):

    def override_urls(self):
        return [
            url(r"^(?P<resource_name>%s)/search%s$" % (
                self._meta.resource_name,
                trailing_slash()),
                self.wrap_view('get_search'),
                name="api_get_search"
            )
        ]

    def get_search(self, request, **kwargs):
        queryset = self.get_object_list(request)
        return self.get_search_in_queryset(queryset, request, **kwargs)

    def get_search_in_queryset(self, queryset, request, **kwargs):
        self.method_check(request, allowed=['get'])
        self.is_authenticated(request)
        self.throttle_check(request)

        queryset = self.get_filtered_queryset(
            queryset,
            request,
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
        queryset = User.objects.all()
        resource_name = 'user'
        authorization = DjangoAuthorization()
        authentication = SessionAuthentication()
        always_return_data = True
        fields = ['username', 'email', 'first_name', 'last_name', 'id']
        validation = FormValidation(form_class=RequesterCreateForm)

    def override_urls(self):
        urls = super(UserResource, self).override_urls()
        return urls + [
            url(r"^agent/search%s$" % (
                trailing_slash()),
                self.wrap_view('get_agent_search'),
                name="api_get_agent_search"
            ),
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

    def get_filtered_queryset(self, queryset, request):
        search_term = request.GET.get('q', '')
        fn_search = search_term
        ln_search = fn_search

        if len(fn_search.split(' ')) == 2:
            fn_search, ln_search = fn_search.split(' ')

        return queryset.filter(
            Q(email__icontains=fn_search) |
            Q(first_name__icontains=fn_search) |
            Q(last_name__icontains=ln_search)
        )

    def obj_create(self, bundle, request=None, **kwargs):
        try:
            User.objects.get(email=bundle.data['email'])
        except User.DoesNotExist:
            pass
        except User.MultipleObjectsReturned:
            raise BadRequest(
                _('A user with this email address already exists')
            )
        else:
            raise BadRequest(
                _('A user with this email address already exists')
            )

        try:
            bundle.obj = User.objects.create_user(
                username=generate_username(),
                email=bundle.data.get('email', None)
            )
            bundle.obj.first_name = bundle.data.get('first_name', None)
            bundle.obj.last_name = bundle.data.get('last_name', None)
            bundle.obj.save()
        except IntegrityError:
            raise BadRequest('That username already exists')
        return bundle


class OrderResource(SearchableModelResource):

    def dehydrate(self, bundle):
        order_label = "Order #%s placed by %s on %s for %s" % (
            bundle.obj.number,
            bundle.obj.email,
            bundle.obj.date_placed.strftime('%Y-%m-%d %H:%M'),
            render_currency(bundle.obj.total_incl_tax),
        )

        bundle.data['label'] = order_label
        bundle.data['value'] = bundle.data['id']
        return bundle

    def get_filtered_queryset(self, queryset, request):
        search_term = request.GET.get('q', '')
        if request.GET.get('user', None):
            queryset = queryset.filter(user__id=request.GET.get('user'))

        return queryset.filter(number__istartswith=search_term)

    class Meta:
        queryset = get_model('order', 'Order').objects.all()
        resource_name = 'order'
        authorization = ReadOnlyAuthorization()
        authentication = SessionAuthentication()


class ProductResource(SearchableModelResource):

    def dehydrate(self, bundle):
        product_label = "%s with UPC %s" % (
            bundle.obj.title,
            bundle.obj.upc,
        )

        image = bundle.obj.primary_image()
        try:
            image = getattr(image, 'original')
        except AttributeError:
            image = image.get('original', None)

        try:
            thumb_image = get_thumbnail(image, "40x40")
        except IOError:
            bundle.data['thumbnail'] = ''
        else:
            bundle.data['thumbnail'] = thumb_image.url

        bundle.data['label'] = product_label
        bundle.data['value'] = bundle.data['id']
        return bundle

    def get_filtered_queryset(self, queryset, request):
        search_term = request.GET.get('q', '')
        return queryset.filter(
            Q(upc__istartswith=search_term) |
            Q(title__icontains=search_term)
        )

    class Meta:
        queryset = get_model('catalogue', 'Product').objects.all()
        resource_name = 'product'
        authorization = ReadOnlyAuthorization()
        authentication = SessionAuthentication()


class LineResource(SearchableModelResource):

    def dehydrate(self, bundle):
        line_label = "Line #%s of order #%s placed by %s on %s for %s" % (
            bundle.obj.id,
            bundle.obj.order.number,
            bundle.obj.order.email,
            bundle.obj.order.date_placed.strftime('%Y-%m-%d %H:%M'),
            render_currency(bundle.obj.order.total_incl_tax),
        )

        bundle.data['label'] = line_label
        bundle.data['value'] = bundle.data['id']
        return bundle

    def get_filtered_queryset(self, queryset, request):
        search_term = request.GET.get('q', '')
        return queryset.filter(
            Q(order__number__istartswith=search_term) |
            Q(product__title__icontains=search_term) |
            Q(product__upc__istartswith=search_term)
        )

    class Meta:
        queryset = get_model('order', 'Line').objects.all()
        resource_name = 'line'
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

    def get_filtered_queryset(self, queryset, request):
        search_term = request.GET.get('q', '')
        return queryset.filter(name__icontains=search_term)


v1_api.register(CommunicationEventTypeResource())
v1_api.register(UserResource())
v1_api.register(ProductResource())
v1_api.register(OrderResource())
v1_api.register(LineResource())
v1_api.register(GroupResource())
