from django import template
from django.conf import settings
from django.db.models import get_model

from oscar_support import defaults

TicketStatus = get_model('oscar_support', 'TicketStatus')

register = template.Library()

SUPPORT_INITIAL_STATUS = getattr(
    settings,
    "SUPPORT_INITIAL_STATUS",
    defaults.SUPPORT_INITIAL_STATUS
)


@register.assignment_tag(takes_context=True)
def get_messages(context, ticket, num_messages=None):
    user = context.get('user', None)
    if not user:
        return []

    if not user.is_staff:
        return get_model('oscar_support', 'Message').objects.filter(ticket=ticket)

    return ticket.messages.select_subclasses()


@register.assignment_tag
def get_ticket_statuses():
    return TicketStatus.objects.all()


@register.assignment_tag
def get_default_ticket_status():
    status, __ = TicketStatus.objects.get_or_create(
        name=SUPPORT_INITIAL_STATUS
    )
    return status
