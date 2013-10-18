from django.views import generic
from django.conf import settings
from django.db.models import get_model
from django.http import HttpResponseRedirect
from django.core.urlresolvers import reverse

from .defaults import SUPPORT_RESOLVED_STATUS
from .forms import TicketUpdateForm, TicketCreateForm

Ticket = get_model('oscar_support', 'Ticket')
Message = get_model('oscar_support', 'Message')
TicketStatus = get_model('oscar_support', 'TicketStatus')

SUPPORT_RESOLVED_STATUS = getattr(
    settings,
    "SUPPORT_RESOLVED_STATUS",
    SUPPORT_RESOLVED_STATUS
)


class TicketListView(generic.ListView):
    model = Ticket
    template_name = 'oscar_support/customer/ticket_list.html'
    context_object_name = 'ticket_list'

    def get_queryset(self, queryset=None):
        # we only want so show top-level tickets for now
        return Ticket.objects.filter(
            requester=self.request.user,
            parent=None,
        )

    def get_context_data(self, **kwargs):
        ctx = super(TicketListView, self).get_context_data(**kwargs)
        status, __ = TicketStatus.objects.get_or_create(
            name=SUPPORT_RESOLVED_STATUS
        )
        ctx['open_ticket_list'] = self.get_queryset().exclude(status=status)
        ctx['resolved_ticket_list'] = self.get_queryset().filter(status=status)
        return ctx


class TicketCreateView(generic.CreateView):
    model = Ticket
    form_class = TicketCreateForm
    context_object_name = 'ticket'
    template_name = 'oscar_support/customer/ticket_create.html'

    def get_form_kwargs(self, **kwargs):
        kwargs = super(TicketCreateView, self).get_form_kwargs(**kwargs)
        kwargs['user'] = self.request.user
        return kwargs

    def get_success_url(self):
        return reverse("support:customer-ticket-list")


class TicketUpdateView(generic.UpdateView):
    model = Ticket
    context_object_name = 'ticket'
    form_class = TicketUpdateForm
    template_name = 'oscar_support/customer/ticket_update.html'

    def form_valid(self, form):
        message_text = form.cleaned_data.get('message_text')
        if not message_text:
            return self.form_invalid(form)
        Message.objects.create(
            ticket=self.object,
            text=message_text,
            user=self.request.user,
        )
        return HttpResponseRedirect(self.get_success_url())

    def get_context_data(self, **kwargs):
        ctx = super(TicketUpdateView, self).get_context_data(**kwargs)
        print "CONTEXT", ctx
        ctx['message_list'] = Message.objects.filter(
            user=self.request.user,
            ticket=self.object,
        )
        return ctx

    def get_success_url(self):
        return reverse(
            "support:customer-ticket-update",
            kwargs={'pk': self.object.uuid}
        )
