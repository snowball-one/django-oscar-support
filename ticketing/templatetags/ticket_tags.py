from django import template
from django.db.models import get_model

register = template.Library()


@register.assignment_tag(takes_context=True)
def get_messages(context, ticket, num_messages=None):
    user = context.get('user', None)
    if not user:
        return []

    if not user.is_staff:
        return get_model('ticketing', 'Message').objects.filter(ticket=ticket)

    return ticket.ticket_messages.select_subclasses()
