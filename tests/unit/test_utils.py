import mock

from django.test import TestCase

from oscar_support.models import Ticket
from oscar_support.utils import TicketNumberGenerator


class TestTheTicketNumberGenerator(TestCase):

    @mock.patch('oscar_support.models.Ticket.objects.count')
    def test_can_generate_a_new_parent_ticket_number(self, subtickets_mock):
        subtickets_mock.return_value = 0

        number_kwargs = TicketNumberGenerator.generate_ticket_number()
        self.assertEquals(number_kwargs['number'], 1)
        self.assertEquals(number_kwargs['subticket_id'], 0)

    @mock.patch('oscar_support.models.Ticket.subtickets')
    def test_can_generate_a_new_subticket_number_for_a_ticket(self,
                                                              subtickets_mock):
        ticket = Ticket()
        ticket.number = "10000"
        subtickets_mock.count = mock.MagicMock(return_value=1)

        number_kwargs = TicketNumberGenerator.generate_subticket_id(ticket)
        self.assertEquals(number_kwargs['number'], ticket.number)
        self.assertEquals(number_kwargs['subticket_id'], 1)
