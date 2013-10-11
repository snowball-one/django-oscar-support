import random

from django.db.models import get_model

from oscar_support.utils import TicketNumberGenerator


User = get_model('auth', 'User')
Ticket = get_model('oscar_support', 'Ticket')
TicketType = get_model('oscar_support', 'TicketType')
TicketStatus = get_model('oscar_support', 'TicketStatus')


# Ticket statuses for testing
TICKET_STATUSES = [
    "New",
    "Open",
    "Pending",
    "Solved",
]

TICKET_TYPES = [
    'Question',
    'Order Inquiry',
]


def create_ticket_statuses():
    for status in TICKET_STATUSES:
        TicketStatus.objects.get_or_create(name=status)


def create_ticket_types():
    for type_name in TICKET_TYPES:
        TicketType.objects.get_or_create(name=type_name)


def create_ticket(requester=None, subject=None, body=None, status=None,
                  type=None, assignee=None, assigned_group=None):
    if not requester:
        try:
            requester = User.objects.get(username='a_customer')
        except User.DoesNotExist:
            requester = User.objects.create_user(username='a_customer',
                                                 email="a_customer@demo.com",
                                                 password="something")

    if not status:
        status, __ = TicketStatus.objects.get_or_create(
            name=random.choice(TICKET_STATUSES)
        )

    if not type:
        type, __ = TicketType.objects.get_or_create(
            name=random.choice(TICKET_TYPES)
        )

    if not subject:
        subject = 'I need help!'

    if not body:
        body = ("I don't have any beer left in the fridge. Can you go "
                "and buy me some? Thanks, The Drinker")

    ticket = Ticket.objects.create(requester=requester, status=status,
                                   type=type, subject=subject, body=body,
                                   assignee=assignee, assigned_group=assigned_group,
                                   **TicketNumberGenerator.generate_ticket_number())
    return ticket
