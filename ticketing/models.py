from django.db import models
from django.utils.translation import ugettext_lazy as _


class TicketType(models.Model):
    name = models.CharField(_("Name"), max_length=64)

    def __unicode__(self):
        return self.name

    class Meta:
        verbose_name = _("Ticket type")
        verbose_name_plural = _("Ticket types")


class TicketStatus(models.Model):
    name = models.CharField(_("Name"), max_length=64)

    def __unicode__(self):
        return self.name

    class Meta:
        verbose_name = _("Ticket status")
        verbose_name_plural = _("Ticket statuses")


class Ticket(models.Model):
    number = models.CharField(_("Number"), max_length=64, db_index=True)
    subticket_number = models.PositiveIntegerField(_("Subticket number"),
                                                   default=0)

    parent = models.ForeignKey('ticketing.Ticket', verbose_name=_("Parent"),
                               related_name="subtickets", null=True, blank=True)

    requester = models.ForeignKey('auth.User', verbose_name=_("Requester"), db_index=True)

    type = models.ForeignKey('ticketing.TicketType', verbose_name=_("Type"),
                             related_name="tickets", db_index=True)

    assignee = models.ForeignKey('auth.User', verbose_name=_("Assignee"), null=True,
                                 blank=True, related_name="tickets")
    assigned_group = models.ForeignKey('auth.Group', verbose_name=_("Assigned group"),
                                       null=True, blank=True, related_name="tickets")

    #FIXME: add tagging capabilities

    # main content of the (initial) ticket
    subject = models.CharField(_("Subject"), max_length=255)
    body = models.TextField(_("Body"))

    is_internal = models.BooleanField(_("Is internal"), default=False)

    date_created = models.DateTimeField(auto_now_add=True)
    date_updated = models.DateTimeField(auto_now=True)

    def __unicode__(self):
        return self.number

    class Meta:
        verbose_name = _("Ticket")
        verbose_name_plural = _("Tickets")


class AbstractMessage(models.Model):
    user = models.ForeignKey('auth.User', verbose_name=_("User"), related_name="%(class)ss")
    ticket = models.ForeignKey('ticketing.Ticket', verbose_name=_("Ticket"),
                               related_name="%(class)ss")

    text = models.TextField(_("Text"))
    date_created = models.DateTimeField(auto_now_add=True)

    def __unicode__(self):
        return "Message from %s for ticket #%s" % (self.user.email,
                                                   self.ticket.number)

    class Meta:
        abstract = True


class Message(AbstractMessage):
    class Meta:
        verbose_name = _("Message")
        verbose_name_plural = _("Messages")


class Note(AbstractMessage):
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
