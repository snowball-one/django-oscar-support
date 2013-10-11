from . import abstract_models as am


class TicketType(am.AbstractTicketType):
    pass


class TicketStatus(am.AbstractTicketStatus):
    pass


class Ticket(am.AbstractTicket):
    pass


class Priority(am.AbstractPriority):
    pass


class Message(am.AbstractMessage):
    pass


class RelatedOrderLine(am.AbstractRelatedOrderLine):
    pass


class RelatedOrder(am.AbstractRelatedOrder):
    pass


class RelatedProduct(am.AbstractRelatedProduct):
    pass


class Attachment(am.AbstractAttachment):
    pass
