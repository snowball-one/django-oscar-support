from django.db.models import get_model

Ticket = get_model('ticketing', 'Ticket')


class TicketNumberGenerator(object):

    @classmethod
    def generate_ticket_number(cls):
        return {
            # we don't want the ticket number to start at zero
            'number': Ticket.objects.count() + 1,
            'subticket_number': 0,
        }

    @classmethod
    def generate_subticket_number(cls, ticket):
        return {
            'number': ticket.number,
            'subticket_number': ticket.subtickets.count(),
        }


class TicketGenerator(object):

    def generate_ticket(self):
        raise NotImplementedError()

    def generate_subtickets(self, ticket):
        raise NotImplementedError()
