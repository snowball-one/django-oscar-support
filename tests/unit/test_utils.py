import mock

from django.test import TestCase

from oscar_support.models import Ticket
from oscar_support.utils import TicketNumberGenerator


class TestTheTicketNumberGenerator(TestCase):

    def test_can_generate_a_new_parent_ticket_number(self):
        with mock.patch('oscar_support.models.Ticket.objects.count') as CountMock:
            CountMock.return_value = 0

            number_kwargs = TicketNumberGenerator.generate_ticket_number()
            self.assertEquals(number_kwargs['number'], 1)
            self.assertEquals(number_kwargs['subticket_number'], 0)

    @mock.patch('oscar_support.models.Ticket.subtickets')
    def test_can_generate_a_new_subticket_number_for_a_ticket(self, subtickets_mock):
        ticket = Ticket()
        ticket.number = "10000"
        subtickets_mock.count = mock.MagicMock(return_value=1)

        number_kwargs = TicketNumberGenerator.generate_subticket_number(ticket)
        self.assertEquals(number_kwargs['number'], ticket.number)
        self.assertEquals(number_kwargs['subticket_number'], 1)
