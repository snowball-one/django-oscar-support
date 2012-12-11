from django import template
from django.conf import settings
from django.db.models import get_model

TicketStatus = get_model('ticketing', 'TicketStatus')

register = template.Library()


@register.assignment_tag(takes_context=True)
def get_messages(context, ticket, num_messages=None):
    user = context.get('user', None)
    if not user:
        return []

    if not user.is_staff:
        return get_model('ticketing', 'Message').objects.filter(ticket=ticket)

    return ticket.messages.select_subclasses()


@register.assignment_tag
def get_ticket_statuses():
    return TicketStatus.objects.all()


@register.assignment_tag
def get_default_ticket_status():
    default_name = getattr(settings, "TICKETING_INITIAL_STATUS", "New")
    status, __ = TicketStatus.objects.get_or_create(
        name=default_name,
    )
    return status
