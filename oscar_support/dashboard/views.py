from django.conf import settings
from django.views import generic
from django.db.models import get_model, Q
from django.http import HttpResponseRedirect
from django.core.urlresolvers import reverse

from . import forms
from .. import defaults

Note = get_model('oscar_support', 'Note')
Ticket = get_model('oscar_support', 'Ticket')
Message = get_model('oscar_support', 'Message')
TicketStatus = get_model('oscar_support', 'TicketStatus')

SUPPORT_INITIAL_STATUS = getattr(
    settings,
    "SUPPORT_INITIAL_STATUS",
    defaults.SUPPORT_INITIAL_STATUS
)

SUPPORT_INITIAL_STATUS_SLUG = getattr(
    settings,
    "SUPPORT_INITIAL_STATUS_SLUG",
    defaults.SUPPORT_INITIAL_STATUS_SLUG
)


class TicketListMixin(object):
    ticket_list = None

    def get_ticket_list(self, queryset=None):
        if self.ticket_list:
            return self.ticket_list

        if queryset is None:
            queryset = self.model.objects.all()

        self.ticket_list = queryset.filter(
            # A user can see tickets that are assigned to them
            # or one of the groups they belong to
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
    template_name = 'oscar_support/dashboard/ticket_detail.html'

    def get_queryset(self, queryset=None):
        return self.get_ticket_list()


class UserFormInlineMixin(object):

    def get_extra_form_kwargs(self):
        kwargs = super(UserFormInlineMixin, self).get_extra_form_kwargs()
        kwargs['user'] = self.request.user
        return kwargs


class TicketCreateView(generic.CreateView):
    model = Ticket
    template_name = 'oscar_support/dashboard/ticket_create.html'
    default_status = None
    form_class = forms.TicketCreateForm

    def get_default_status(self):
        if self.default_status:
            return self.default_status

        try:
            self.default_status = TicketStatus.objects.get(
                slug=SUPPORT_INITIAL_STATUS_SLUG
            )
        except TicketStatus.DoesNotExist:
            self.default_status = TicketStatus.objects.create(
                slug=SUPPORT_INITIAL_STATUS_SLUG,
                name=SUPPORT_INITIAL_STATUS
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
        ctx['requester_create_form'] = forms.RequesterCreateForm()
        return ctx

    def get_success_url(self, **kwargs):
        return reverse("support-dashboard:ticket-list")


class TicketUpdateView(TicketListMixin, generic.UpdateView):
    model = Ticket
    default_message_model = Message
    context_object_name = 'selected_ticket'
    form_class = forms.TicketUpdateForm
    template_name = 'oscar_support/dashboard/ticket_detail.html'

    def get_context_data(self, **kwargs):
        ctx = super(TicketUpdateView, self).get_context_data(**kwargs)
        ctx['ticket_list'] = self.get_ticket_list()
        return ctx

    def form_valid(self, form):
        ticket = form.save()
        message_type = form.cleaned_data.get('message_type', Message.PUBLIC)
        message_text = form.cleaned_data.get('message_text')
        Message.objects.create(
            user=self.request.user,
            type=message_type,
            text=message_text,
            ticket=ticket
        )
        return HttpResponseRedirect(self.get_success_url())

    def get_success_url(self):
        return reverse("support-dashboard:ticket-list")
