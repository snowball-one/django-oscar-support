from django import forms
from django.db.models import get_model
from django.utils.translation import ugettext_lazy as _

from oscar.templatetags.currency_filters import currency

from ticketing import TICKETING_INITIAL_STATUS

Order = get_model('order', 'Order')
RelatedOrder = get_model("ticketing", "RelatedOrder")
TicketStatus = get_model("ticketing", "TicketStatus")


class TicketUpdateForm(forms.ModelForm):
    message_text = forms.CharField(label=_("Message"), widget=forms.Textarea())

    class Meta:
        model = get_model("ticketing", "Ticket")
        fields = ['message_text']


class TicketCreateForm(forms.ModelForm):
    order = forms.ChoiceField(
        label=_("Related to order"),
        required=False
    )

    def __init__(self, user, *args, **kwargs):
        super(TicketCreateForm, self).__init__(*args, **kwargs)
        self.user = user

        order_choices = [(0, _('Not related to an order'))]
        for order in Order.objects.filter(user=self.user).order_by('date_placed'):
            label = _("Order #%s for %s") % (
                order.number,
                currency(order.total_incl_tax)
            )
            order_choices.append((order.id, label))

        self.fields['order'].choices = order_choices

    def save(self, commit=True):
        instance = super(TicketCreateForm, self).save(commit=False)

        initial_status, __ = TicketStatus.objects.get_or_create(
            name=TICKETING_INITIAL_STATUS,
        )
        instance.status = initial_status
        instance.requester = self.user

        if commit:
            instance.save()

        order_id = self.cleaned_data['order']
        if order_id:
            try:
                order = Order.objects.get(id=order_id)
            except Order.DoesNotExist:
                pass
            else:
                instance.save()
                RelatedOrder.objects.create(ticket=instance, order=order)

        return instance

    class Meta:
        model = get_model("ticketing", "Ticket")
        fields = ['type', 'subject', 'body']
