from django.db.models import get_model
from oscar_support import defaults


class TicketNumberGenerator(object):

    @classmethod
    def generate_ticket_number(cls):
        return {
            # we don't want the ticket number to start at zero
            'number': get_model('oscar_support', 'Ticket').objects.count() + 1,
            'subticket_id': 0,
        }

    @classmethod
    def generate_subticket_id(cls, ticket):
        return {
            'number': ticket.number,
            'subticket_id': ticket.subtickets.count(),
        }


class TicketGenerator(object):

    def generate_ticket(self):
        raise NotImplementedError()

    def generate_subtickets(self, ticket):
        raise NotImplementedError()


class TicketStatusGenerator(object):
    @classmethod
    def get_initial_status(cls):
        TicketStatus = get_model("oscar_support", "TicketStatus")
        try:
            initial_status = TicketStatus.objects.get(
                slug=defaults.SUPPORT_INITIAL_STATUS_SLUG
            )
        except TicketStatus.DoesNotExist:
            initial_status = TicketStatus.objects.create(
                slug=defaults.SUPPORT_INITIAL_STATUS_SLUG,
                name=defaults.SUPPORT_INITIAL_STATUS
            )
        return initial_status

    @classmethod
    def get_resolved_status(cls):
        TicketStatus = get_model("oscar_support", "TicketStatus")
        try:
            resolved_status = TicketStatus.objects.get(
                slug=defaults.SUPPORT_RESOLVED_STATUS_SLUG
            )
        except TicketStatus.DoesNotExist:
            resolved_status = TicketStatus.objects.create(
                slug=defaults.SUPPORT_RESOLVED_STATUS_SLUG,
                name=defaults.SUPPORT_RESOLVED_STATUS
            )
        return resolved_status
