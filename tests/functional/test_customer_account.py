from django.core.urlresolvers import reverse

from oscar.test.testcases import WebTestCase

from oscar_support.models import Ticket
from oscar_support.defaults import SUPPORT_INITIAL_STATUS

from tests import factories


class TestACustomer(WebTestCase):
    is_anonymous = False

    def setUp(self):
        super(TestACustomer, self).setUp()

        self.status = factories.TicketStatusFactory(
            name=SUPPORT_INITIAL_STATUS
        )
        self.type = factories.TicketTypeFactory()

        self.subject = "this is the subject line"
        self.message_text = "this is a new message text"

    def test_can_create_a_new_ticket(self):
        page = self.get(reverse('support:customer-ticket-create'))

        ticket_form = page.forms['create-ticket-form']
        ticket_form['type'] = self.type.uuid
        ticket_form['subject'] = self.subject
        ticket_form['body'] = self.message_text
        page = ticket_form.submit()

        user_tickets = Ticket.objects.filter(requester=self.user)
        self.assertEquals(user_tickets.count(), 1)

        ticket = user_tickets[0]
        self.assertEquals(ticket.status, self.status)
        self.assertEquals(ticket.type, self.type)
        self.assertEquals(ticket.subject, self.subject)
        self.assertEquals(ticket.body, self.message_text)
        self.assertEquals(ticket.number, '1')
        self.assertEquals(ticket.subticket_id, 0)
        self.assertEquals(ticket.relatedorders.count(), 0)

    def test_can_create_a_ticket_with_related_order(self):
        page = self.get(reverse('support:customer-ticket-create'))

        ticket_form = page.forms['create-ticket-form']
        ticket_form['type'] = self.type.uuid
        ticket_form['subject'] = self.subject
        ticket_form['body'] = self.message_text
        page = ticket_form.submit()

        user_tickets = Ticket.objects.filter(requester=self.user)
        self.assertEquals(user_tickets.count(), 1)

        ticket = user_tickets[0]
        self.assertEquals(ticket.status, self.status)
        self.assertEquals(ticket.type, self.type)
        self.assertEquals(ticket.subject, self.subject)
        self.assertEquals(ticket.body, self.message_text)
        self.assertEquals(ticket.number, '1')
        self.assertEquals(ticket.subticket_id, 0)

    def test_can_add_message_to_a_ticket(self):
        ticket = Ticket.objects.create(
            requester=self.user,
            status=self.status,
            type=self.type,
            subject='This is the subject line',
            body="I have a question about something",
        )
        self.assertEquals(ticket.messages.count(), 0)

        page = self.get(
            reverse(
                'support:customer-ticket-update',
                kwargs={'pk': ticket.uuid}
            )
        )
        self.assertContains(page, ticket.body)

        message_form = page.forms['add-message-form']
        message_form['message_text'] = 'this is some additional message'
        message_form.submit()

        ticket = Ticket.objects.get(uuid=ticket.uuid)
        self.assertEquals(ticket.messages.count(), 1)
