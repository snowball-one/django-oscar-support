from django.db import models
from django.utils.translation import ugettext_lazy as _

from model_utils.managers import InheritanceManager


class TicketType(models.Model):
    name = models.CharField(_("Name"), max_length=64, unique=True)

    def __unicode__(self):
        return self.name

    class Meta:
        verbose_name = _("Ticket type")
        verbose_name_plural = _("Ticket types")


class TicketStatus(models.Model):
    name = models.CharField(_("Name"), max_length=64, unique=True)

    def __unicode__(self):
        return self.name

    class Meta:
        verbose_name = _("Ticket status")
        verbose_name_plural = _("Ticket statuses")


class Ticket(models.Model):
    number = models.CharField(_("Number"), max_length=64, unique=True,
                              db_index=True)
    subticket_number = models.PositiveIntegerField(_("Subticket number"),
                                                   default=0)

    parent = models.ForeignKey('ticketing.Ticket', verbose_name=_("Parent"),
                               related_name="subtickets",
                               null=True, blank=True)

    requester = models.ForeignKey('auth.User', verbose_name=_("Requester"),
                                  db_index=True)

    status = models.ForeignKey('ticketing.TicketStatus', db_index=True,
                               verbose_name=_("Status"),
                               related_name="tickets")
    type = models.ForeignKey('ticketing.TicketType', verbose_name=_("Type"),
                             related_name="tickets", db_index=True)

    assignee = models.ForeignKey('auth.User', verbose_name=_("Assignee"),
                                 null=True, blank=True, related_name="tickets")
    assigned_group = models.ForeignKey('auth.Group',
                                       verbose_name=_("Assigned group"),
                                       related_name="tickets", null=True,
                                       blank=True)

    #FIXME: add tagging capabilities

    # main content of the (initial) ticket
    subject = models.CharField(_("Subject"), max_length=255)
    body = models.TextField(_("Body"))

    is_internal = models.BooleanField(_("Internal ticket"), default=False,
        help_text=_("use this ticket only internally and don't display to "
                    "the customer"))

    date_created = models.DateTimeField(auto_now_add=True)
    date_updated = models.DateTimeField(auto_now=True)

    @property
    def printable_number(self):
        return "%s-%s" % (self.number, self.subticket_number)

    def __unicode__(self):
        return "Ticket #%s-%s" % (self.number, self.subticket_number)

    class Meta:
        # we want the oldest tickets to be first in the queue so that
        # they get updated before newer ones (FIFO queue handling)
        ordering = ['-date_updated']
        verbose_name = _("Ticket")
        verbose_name_plural = _("Tickets")


class BaseMessage(models.Model):
    is_internal = False

    user = models.ForeignKey('auth.User', verbose_name=_("User"),
                             related_name="ticket_messages")
    ticket = models.ForeignKey('ticketing.Ticket', verbose_name=_("Ticket"),
                               related_name="ticket_messages")

    text = models.TextField(_("Text"))
    date_created = models.DateTimeField(auto_now_add=True)

    objects = InheritanceManager()

    def __unicode__(self):
        return "Message from %s for ticket #%s" % (self.user.email,
                                                   self.ticket.number)

    class Meta:
        ordering = ['-date_created']


class Message(BaseMessage):

    class Meta:
        verbose_name = _("Response")
        verbose_name_plural = _("Response")


class Note(BaseMessage):
    is_internal = True

    class Meta:
        verbose_name = _("Note")
        verbose_name_plural = _("Notes")


class AbstractRelatedItem(models.Model):
    ticket = models.ForeignKey('ticketing.Ticket', verbose_name=_("Ticket"),
                               related_name="related_%(class)ss")

    class Meta:
        abstract = True
        verbose_name = _("Related item")
        verbose_name_plural = _("Related items")


class RelatedOrder(AbstractRelatedItem):
    order = models.ForeignKey('order.Order', verbose_name=_("Order"))

    class Meta:
        verbose_name = _("Related order")
        verbose_name_plural = _("Related orders")


class RelatedLine(AbstractRelatedItem):
    line = models.ForeignKey('order.Line', verbose_name=_("Line"))

    class Meta:
        verbose_name = _("Related line")
        verbose_name_plural = _("Related lines")


class RelatedProduct(AbstractRelatedItem):
    order = models.ForeignKey('catalogue.Product', verbose_name=_("Product"))

    class Meta:
        verbose_name = _("Related product")
        verbose_name_plural = _("Related products")


class RelatedFile(AbstractRelatedItem):
    file = models.FileField(upload_to="ticketing/%Y/%m", verbose_name=_("File"))

    class Meta:
        verbose_name = _("Related file")
        verbose_name_plural = _("Related files")
