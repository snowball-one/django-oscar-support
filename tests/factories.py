import factory
import humanize

from django.db.models import get_model

from oscar.core.compat import get_user_model


Message = get_model('oscar_support', 'Message')


PRIORITIES = ['High', 'Medium', 'Low']
TICKET_STATUSES = ["New", "Open", "Pending", "Solved"]
TICKET_TYPES = ['Question', 'Order Inquiry']


class UserFactory(factory.DjangoModelFactory):
    FACTORY_FOR = get_user_model()

    username = factory.Sequence(
        lambda n: "Peter The {0}".format(humanize.apnumber(n))
    )


class StaffUserFactory(UserFactory):
    is_staff = True


class CustomerFactory(UserFactory):
    username = factory.Sequence(lambda n: "customer{0}".format(n))
    email = factory.Sequence(lambda n: "customer{0}@example.com".format(n))


class TicketStatusFactory(factory.DjangoModelFactory):
    FACTORY_FOR = get_model('oscar_support', 'TicketStatus')

    name = factory.Sequence(
        lambda n: TICKET_STATUSES[n % len(TICKET_STATUSES)]
    )


class TicketTypeFactory(factory.DjangoModelFactory):
    FACTORY_FOR = get_model('oscar_support', 'TicketType')

    name = factory.Sequence(lambda n: TICKET_TYPES[n % len(TICKET_TYPES)])


class PriorityFactory(factory.DjangoModelFactory):
    FACTORY_FOR = get_model('oscar_support', 'Priority')

    name = factory.Sequence(lambda n: PRIORITIES[n % len(PRIORITIES)])


class TicketFactory(factory.DjangoModelFactory):
    FACTORY_FOR = get_model('oscar_support', 'Ticket')

    status = factory.SubFactory(TicketStatusFactory)
    type = factory.SubFactory(TicketTypeFactory)
    priority = factory.SubFactory(PriorityFactory)
    requester = factory.SubFactory(UserFactory)

    subject = factory.LazyAttribute(
        lambda a: "{0} needs help with something".format(a.requester.username)
    )
    body = factory.LazyAttribute(
        lambda a: "I have a problem, can you help? {0}".format(
            a.requester.username
        )
    )


class MessageFactory(factory.DjangoModelFactory):
    FACTORY_FOR = Message

    type = Message.PUBLIC


class InternalNoteFactory(MessageFactory):
    type = Message.INTERNAL
    user = factory.SubFactory(StaffUserFactory)
    ticket = factory.SubFactory(TicketFactory)
    text = factory.LazyAttributeSequence(
        lambda a, n: "Internal message {0} from {1}".format(n, a.user)
    )


class CustomerMessageFactory(MessageFactory):
    text = factory.LazyAttributeSequence(
        lambda a, n: "Message {0} from customer {1}".format(n, a.user)
    )
