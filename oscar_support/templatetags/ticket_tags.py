from django import template
from django.db.models import get_model

from oscar_support import utils

Message = get_model('oscar_support', 'Message')
TicketStatus = get_model('oscar_support', 'TicketStatus')

register = template.Library()


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
    return utils.TicketStatusGenerator.get_initial_status()
