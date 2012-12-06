from django.db.models import get_model
from django.core.urlresolvers import reverse

from tests import helpers
from oscar_testsupport.testcases import WebTestCase

User = get_model('auth', 'User')
Group = get_model('auth', 'Group')
Ticket = get_model('ticketing', 'Ticket')
TicketType = get_model('ticketing', 'TicketType')
TicketStatus = get_model('ticketing', 'TicketStatus')

Message = get_model('ticketing', 'Message')
Note = get_model('ticketing', 'Note')


class TestAStaffMember(WebTestCase):
    is_staff = True

    def setUp(self):
        super(TestAStaffMember, self).setUp()
        self.support_group = Group.objects.create(name='Support')
        self.tech_group = Group.objects.create(name='Tech Support')
        self.reject_group = Group.objects.create(name='Reject Group')

        self.user.groups.add(self.support_group)
        self.user.groups.add(self.tech_group)

        helpers.create_ticket_statuses()
        helpers.create_ticket_types()

    def tearDown(self):
        super(TestAStaffMember, self).tearDown()
        TicketType.objects.all().delete()
        TicketStatus.objects.all().delete()

    def test_can_see_unassigned_ticket(self):
        self.unassigned_ticket = helpers.create_ticket()
        self.hidden_ticket = helpers.create_ticket(
            assigned_group=self.reject_group)

        page = self.get(reverse('ticketing-dashboard:ticket-list'))
        ticket_list = page.context[0]['ticket_list']

        self.assertEquals(len(ticket_list), 1)
        self.assertEquals(ticket_list[0].number, '1')

        self.assertContains(page, self.unassigned_ticket.printable_number)
        self.assertNotContains(page, self.hidden_ticket.printable_number)

    def test_can_create_a_new_ticket_for_an_existing_user(self):
        customer = User.objects.create_user(username="customer_one",
                                            email="customer1@example.com",
                                            password="somepassword")
        question_type = TicketType.objects.get(name="Question")

        page = self.get(reverse('ticketing-dashboard:ticket-create'))
        ticket_form = page.form
        ticket_form['requester'] = customer.id
        ticket_form['type'] = question_type.id
        ticket_form['subject'] = 'this is my subject'
        ticket_form['body'] = 'the actual message'
        ticket_form.submit()

        ticket = Ticket.objects.get(requester=customer)
        self.assertEquals(ticket.number, "1")
        self.assertEquals(ticket.subticket_number, 0)
        self.assertEquals(ticket.status.name, 'New')
        self.assertEquals(ticket.type, question_type)

    def test_can_create_an_open_ticket_for_an_existing_user(self):
        customer = User.objects.create_user(username="customer_one",
                                            email="customer1@example.com",
                                            password="somepassword")
        question_type = TicketType.objects.get(name="Question")
        status = TicketStatus.objects.get(name="Open")

        page = self.get(reverse('ticketing-dashboard:ticket-create'))
        ticket_form = page.form
        ticket_form['requester'] = customer.id
        ticket_form['status'] = status.id
        ticket_form['type'] = question_type.id
        ticket_form['subject'] = 'this is my subject'
        ticket_form['body'] = 'the actual message'
        ticket_form.submit()

        ticket = Ticket.objects.get(requester=customer)
        self.assertEquals(ticket.number, "1")
        self.assertEquals(ticket.subticket_number, 0)
        self.assertEquals(ticket.status, status)
        self.assertEquals(ticket.type, question_type)


class TestATicket(WebTestCase):
    is_staff = True

    def setUp(self):
        super(TestATicket, self).setUp()
        self.support_group = Group.objects.create(name='Support')
        self.user.groups.add(self.support_group)

        self.customer = User.objects.create_user(username='customer',
                                                 email='customer@buymore.com',
                                                 password='something')
        self.ticket = helpers.create_ticket(assigned_group=self.support_group,
                                            requester=self.customer)

        helpers.create_ticket_statuses()
        helpers.create_ticket_types()

    def test_can_be_displayed_with_all_messages(self):
        note = Note.objects.create(user=self.user, ticket=self.ticket,
                                   text="This is an internal message for the ticket.")
        msg = Message.objects.create(user=self.user, ticket=self.ticket,
                                     text="Now I am telling the customer something.")
        reply = Message.objects.create(user=self.customer, ticket=self.ticket,
                                       text="I am the customer and shout at you.")

        page = self.get(reverse('ticketing-dashboard:ticket-update',
                                args=(self.ticket.id,)))
        self.assertContains(page, self.ticket.printable_number)
        self.assertContains(page, note.text)
        self.assertContains(page, msg.text)
        self.assertContains(page, reply.text)

    def test_can_be_updated_with_an_internal_note(self):
        message_text = "I am adding an internal message"
        page = self.get(reverse('ticketing-dashboard:ticket-update',
                                args=(self.ticket.id,)))

        update_form = page.forms['ticket-update-form']
        update_form['message_text'] = message_text
        update_form['message_type'] = "note"
        page = update_form.submit()

        self.assertRedirects(page, reverse('ticketing-dashboard:ticket-list'))
        self.assertEquals(self.ticket.messages.count(), 1)

        message = self.ticket.messages.select_subclasses()[0]
        self.assertEquals(message.__class__, Note)
        self.assertEquals(message.text, message_text)
        self.assertEquals(message.user, self.user)

    def test_can_be_updated_with_a_public_response(self):
        message_text = "I am adding a public message or reply"
        page = self.get(reverse('ticketing-dashboard:ticket-update',
                                args=(self.ticket.id,)))

        update_form = page.forms['ticket-update-form']
        update_form['message_text'] = message_text
        page = update_form.submit()

        self.assertRedirects(page, reverse('ticketing-dashboard:ticket-list'))
        self.assertEquals(self.ticket.messages.count(), 1)

        message = self.ticket.messages.select_subclasses()[0]
        self.assertEquals(message.__class__, Message)
        self.assertEquals(message.text, message_text)
        self.assertEquals(message.user, self.user)
