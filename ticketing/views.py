from django.views import generic
from django.db.models import get_model
from django.http import HttpResponseRedirect
from django.core.urlresolvers import reverse

from ticketing.forms import TicketUpdateForm, TicketCreateForm

Ticket = get_model('ticketing', 'Ticket')
Message = get_model('ticketing', 'Message')
TicketStatus = get_model('ticketing', 'TicketStatus')


class TicketListView(generic.ListView):
    model = Ticket
    template_name = 'ticketing/customer/list.html'
    context_object_name = 'ticket_list'

    def get_queryset(self, queryset=None):
        # we only want so show top-level tickets for now
        return Ticket.objects.filter(
            requester=self.request.user,
            parent=None,
        )

    def get_context_data(self, **kwargs):
        ctx = super(TicketListView, self).get_context_data(**kwargs)
        status, __ = TicketStatus.objects.get_or_create(name="Resolved")
        ctx['open_ticket_list'] = self.get_queryset().exclude(status=status)
        ctx['resolved_ticket_list'] = self.get_queryset().filter(status=status)
        return ctx


class TicketCreateView(generic.CreateView):
    model = Ticket
    form_class = TicketCreateForm
    context_object_name = 'ticket'
    template_name = 'ticketing/customer/ticket_create.html'

    def get_form_kwargs(self, **kwargs):
        kwargs = super(TicketCreateView, self).get_form_kwargs(**kwargs)
        kwargs['user'] = self.request.user
        return kwargs

    def get_success_url(self):
        return reverse("ticketing:customer-ticket-list")


class TicketUpdateView(generic.UpdateView):
    model = Ticket
    context_object_name = 'ticket'
    form_class = TicketUpdateForm
    template_name = 'ticketing/customer/ticket_update.html'

    def form_valid(self, form):
        message_text = form.cleaned_data['message_text']

        Message.objects.create(
            ticket=self.object,
            text=message_text,
            user=self.request.user,
        )

        return HttpResponseRedirect(self.get_success_url())

    def get_context_data(self, **kwargs):
        ctx = super(TicketUpdateView, self).get_context_data(**kwargs)
        ctx['message_list'] = Message.objects.filter(
            user=self.request.user,
            ticket=self.object,
        )
        return ctx

    def get_success_url(self):
        return reverse("ticketing:customer-ticket-update",
                       args=(self.object.id,))
