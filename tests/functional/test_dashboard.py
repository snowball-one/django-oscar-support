from django.db.models import get_model
from django.core.urlresolvers import reverse

from tests import factories
from oscar.test.testcases import WebTestCase

User = get_model('auth', 'User')
Group = get_model('auth', 'Group')
Ticket = get_model('oscar_support', 'Ticket')
Message = get_model('oscar_support', 'Message')
TicketType = get_model('oscar_support', 'TicketType')
TicketStatus = get_model('oscar_support', 'TicketStatus')


class TestAStaffMember(WebTestCase):
    is_staff = True

    def setUp(self):
        super(TestAStaffMember, self).setUp()
        self.support_group = Group.objects.create(name='Support')
        self.tech_group = Group.objects.create(name='Tech Support')
        self.reject_group = Group.objects.create(name='Reject Group')

    def test_can_see_unassigned_ticket(self):
        unassigned_ticket = factories.TicketFactory()
        hidden_ticket = factories.TicketFactory(
            assigned_group=self.reject_group
        )

        page = self.get(reverse('support-dashboard:ticket-list'))
        ticket_list = page.context[0]['ticket_list']

        self.assertEquals(len(ticket_list), 1)
        self.assertEquals(ticket_list[0].number, '1')
        self.assertContains(
            page,
            "#{0}".format(unassigned_ticket.printable_number)
        )
        self.assertNotContains(
            page,
            "#{0}".format(hidden_ticket.printable_number)
        )

    def test_can_create_a_new_ticket_for_an_existing_user(self):
        customer = factories.CustomerFactory()
        ticket_type = factories.TicketTypeFactory()

        page = self.get(reverse('support-dashboard:ticket-create'))
        ticket_form = page.forms['ticket-create-form']
        ticket_form['requester'] = customer.id
        ticket_form['type'] = ticket_type.uuid
        ticket_form['subject'] = 'this is my subject'
        ticket_form['body'] = 'the actual message'
        ticket_form.submit(name='status', index=0)

        ticket = Ticket.objects.get(requester=customer)
        self.assertEquals(ticket.number, "1")
        self.assertEquals(ticket.subticket_id, 0)
        self.assertEquals(ticket.status.name, 'New')
        self.assertEquals(ticket.type, ticket_type)

    def test_can_create_an_open_ticket_for_an_existing_user(self):
        customer = factories.CustomerFactory()
        ticket_type = factories.TicketTypeFactory()
        status = factories.TicketStatusFactory()

        page = self.get(reverse('support-dashboard:ticket-create'))
        ticket_form = page.forms['ticket-create-form']
        ticket_form['requester'] = customer.id
        ticket_form['type'] = ticket_type.uuid
        ticket_form['subject'] = 'this is my subject'
        ticket_form['body'] = 'the actual message'
        ticket_form.submit(name='status', index=1)

        ticket = Ticket.objects.get(requester=customer)
        self.assertEquals(ticket.number, "1")
        self.assertEquals(ticket.subticket_id, 0)
        self.assertEquals(ticket.status, status)
        self.assertEquals(ticket.type, ticket_type)


class TestATicket(WebTestCase):
    is_staff = True

    def setUp(self):
        super(TestATicket, self).setUp()
        self.support_group = Group.objects.create(name='Support')
        self.user.groups.add(self.support_group)

        self.customer = factories.CustomerFactory()

        self.ticket = factories.TicketFactory(
            assigned_group=self.support_group,
            requester=self.customer
        )

    def test_can_be_displayed_with_all_messages(self):
        note = factories.InternalNoteFactory(
            user=self.user,
            ticket=self.ticket
        )
        msg = factories.MessageFactory(user=self.user, ticket=self.ticket)
        reply = factories.CustomerMessageFactory(
            ticket=self.ticket,
            user=self.customer
        )

        page = self.get(
            reverse(
                'support-dashboard:ticket-update',
                kwargs={'pk': self.ticket.uuid}
            )
        )
        self.assertContains(page, self.ticket.printable_number)
        self.assertContains(page, note.text)
        self.assertContains(page, msg.text)
        self.assertContains(page, reply.text)

    def test_can_be_updated_with_an_internal_note(self):
        message_text = "I am adding an internal message"
        page = self.get(
            reverse(
                'support-dashboard:ticket-update',
                kwargs={'pk': self.ticket.uuid}
            )
        )
        update_form = page.forms['ticket-update-form']
        update_form['message_text'] = message_text
        update_form['message_type'] = Message.INTERNAL
        page = update_form.submit()

        self.assertRedirects(page, reverse('support-dashboard:ticket-list'))
        self.assertEquals(self.ticket.messages.count(), 1)

        message = self.ticket.messages.all()[0]
        self.assertEquals(message.type, Message.INTERNAL)
        self.assertEquals(message.text, message_text)
        self.assertEquals(message.user, self.user)

    def test_can_be_updated_with_a_public_response(self):
        message_text = "I am adding a public message or reply"
        page = self.get(
            reverse(
                'support-dashboard:ticket-update',
                kwargs={'pk': self.ticket.uuid}
            )
        )

        update_form = page.forms['ticket-update-form']
        update_form['message_text'] = message_text
        page = update_form.submit()

        self.assertRedirects(page, reverse('support-dashboard:ticket-list'))
        self.assertEquals(self.ticket.messages.count(), 1)

        message = self.ticket.messages.all()[0]
        self.assertEquals(message.type, Message.PUBLIC)
        self.assertEquals(message.text, message_text)
        self.assertEquals(message.user, self.user)
