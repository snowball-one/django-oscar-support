import mock

from django.test import TestCase

from oscar_support import defaults
from oscar_support.models import Ticket, TicketStatus
from oscar_support.utils import TicketNumberGenerator, TicketStatusGenerator


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


class TestTheStatusGenerator(TestCase):

    def test_returns_initial_status(self):
        initial_status = TicketStatusGenerator.get_initial_status()
        self.assertIsInstance(initial_status, TicketStatus)
        self.assertEquals(
            defaults.SUPPORT_INITIAL_STATUS,
            initial_status.name
        )
        self.assertEquals(
            defaults.SUPPORT_INITIAL_STATUS_SLUG,
            initial_status.slug
        )

    def test_returns_resolved_status(self):
        resolved_status = TicketStatusGenerator.get_resolved_status()
        self.assertIsInstance(resolved_status, TicketStatus)
        self.assertEquals(
            defaults.SUPPORT_RESOLVED_STATUS,
            resolved_status.name
        )
        self.assertEquals(
            defaults.SUPPORT_RESOLVED_STATUS_SLUG,
            resolved_status.slug
        )
