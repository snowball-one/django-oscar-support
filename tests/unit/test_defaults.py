from django.test import TestCase

from oscar_support.models import TicketStatus
from oscar_support import defaults


class TestDefaults(TestCase):

    def test_returns_initial_status(self):
        initial_status = defaults.get_ticket_initial_status()
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
        resolved_status = defaults.get_ticket_resolved_status()
        self.assertIsInstance(resolved_status, TicketStatus)
        self.assertEquals(
            defaults.SUPPORT_RESOLVED_STATUS,
            resolved_status.name
        )
        self.assertEquals(
            defaults.SUPPORT_RESOLVED_STATUS_SLUG,
            resolved_status.slug
        )
