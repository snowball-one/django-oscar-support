from django.db.models import get_model
from django.contrib.sites.models import Site
from django.template import Template, RequestContext

from tastypie import fields
from tastypie.api import Api
from tastypie.constants import ALL_WITH_RELATIONS
from tastypie.resources import ModelResource
from tastypie.authorization import ReadOnlyAuthorization

from ticketing.api.authentication import SessionAuthentication

v1_api = Api(api_name='v1')


Ticket = get_model('ticketing', 'Ticket')


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

class UserResource(ModelResource):
    class Meta:
        queryset = get_model('auth', 'User').objects.all()
        resource_name = 'user'
        authorization = ReadOnlyAuthorization()
        authentication = SessionAuthentication()


class OrderResource(ModelResource):
    user = fields.ForeignKey(UserResource, 'user')

    class Meta:
        queryset = get_model('order', 'Order').objects.all()
        resource_name = 'order'
        authorization = ReadOnlyAuthorization()
        authentication = SessionAuthentication()
        filtering = {
            'user': ALL_WITH_RELATIONS,
        }


v1_api.register(CommunicationEventTypeResource())
v1_api.register(UserResource())
v1_api.register(OrderResource())
