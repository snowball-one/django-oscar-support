from django.conf import settings
from django.views import generic
from django.db.models import get_model, Q
from django.http import HttpResponseRedirect
from django.core.urlresolvers import reverse
from django.utils.translation import ugettext as _

from ticketing.dashboard import forms
from ticketing.utils import TicketNumberGenerator

Note = get_model('ticketing', 'Note')
Ticket = get_model('ticketing', 'Ticket')
Message = get_model('ticketing', 'Message')
TicketStatus = get_model('ticketing', 'TicketStatus')


class TicketListMixin(object):
    ticket_list = None

    def get_ticket_list(self, queryset=None):
        if self.ticket_list:
            return self.ticket_list

        if queryset is None:
            queryset = self.model.objects.all()

        self.ticket_list = queryset.filter(
            # A user can see tickets that are assigned to them
            # or on of the groups they belong to
            Q(assignee=self.request.user) |
            Q(assigned_group__in=self.request.user.groups.all()) |
            # they can also see tickets that have no assigned
            # group AND user
            Q(assignee=None, assigned_group=None)
        )
        return self.ticket_list


class TicketListView(TicketListMixin, generic.ListView):
    model = Ticket
    context_object_name = 'ticket_list'
    template_name = 'ticketing/dashboard/ticket_detail.html'

    def get_queryset(self, queryset=None):
        return self.get_ticket_list()


class TicketCreateView(generic.CreateView):
    model = Ticket
    template_name = 'ticketing/dashboard/ticket_create.html'
    default_status = None
    form_class = forms.TicketCreateForm

    def form_valid(self, form):
        ticket_numbers = TicketNumberGenerator.generate_ticket_number()

        ticket = form.save(commit=False)
        ticket.number = ticket_numbers['number']
        ticket.subticket_number = ticket_numbers['subticket_number']
        ticket.save()

        return HttpResponseRedirect(self.get_success_url())

    def get_default_status(self):
        if self.default_status:
            return self.default_status

        self.default_status, __ = TicketStatus.objects.get_or_create(
            name=getattr(settings, 'TICKETING_DEFAULT_STATUS', _("New")),
        )
        return self.default_status

    def get_form_kwargs(self):
        kwargs = super(TicketCreateView, self).get_form_kwargs()
        kwargs['initial'].update({'status': self.get_default_status()})
        return kwargs

    def get_context_data(self, **kwargs):
        ctx = super(TicketCreateView, self).get_context_data(**kwargs)
        status = self.get_default_status()
        ctx['default_status'] = status
        ctx['status_list'] = TicketStatus.objects.exclude(name=status.name)
        return ctx

    def get_success_url(self, **kwargs):
        return reverse("ticketing-dashboard:ticket-list")


class TicketUpdateView(TicketListMixin, generic.UpdateView):
    model = Ticket
    default_message_model = Message
    context_object_name = 'selected_ticket'
    form_class = forms.TicketUpdateForm
    template_name = 'ticketing/dashboard/ticket_detail.html'

    def get_context_data(self, **kwargs):
        ctx = super(TicketUpdateView, self).get_context_data(**kwargs)
        ctx['ticket_list'] = self.get_ticket_list()
        return ctx

    def form_valid(self, form):
        ticket = form.save()

        message_type = form.cleaned_data.get('message_type', None)
        message_text = form.cleaned_data.get('message_text', None)

        if message_type and message_text:
            message_model = self.default_message_model
            if message_type == 'note':
                message_model = Note

            message_model.objects.create(user=self.request.user,
                                         text=message_text, ticket=ticket)

        return HttpResponseRedirect(self.get_success_url())

    def get_success_url(self):
        return reverse("ticketing-dashboard:ticket-list")
