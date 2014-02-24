from django import template
from django.conf import settings
from django.db.models import get_model

from oscar_support import defaults

Message = get_model('oscar_support', 'Message')
TicketStatus = get_model('oscar_support', 'TicketStatus')

register = template.Library()

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


@register.assignment_tag(takes_context=True)
def get_messages(context, ticket, num_messages=None):
    user = context.get('user', None)
    if not user:
        return []
    if not user.is_staff:
        return Message.objects.filter(ticket=ticket, type=Message.PUBLIC)
    return ticket.messages.all()


@register.assignment_tag
def get_ticket_statuses():
    return TicketStatus.objects.all()


@register.assignment_tag
def get_default_ticket_status():
    try:
        status = TicketStatus.objects.get(
            slug=SUPPORT_INITIAL_STATUS_SLUG
        )
    except TicketStatus.DoesNotExist:
        status = TicketStatus.objects.create(
            slug=SUPPORT_INITIAL_STATUS_SLUG,
            name=SUPPORT_INITIAL_STATUS
        )
    return status
