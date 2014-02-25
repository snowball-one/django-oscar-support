from django import forms
from django.db.models import get_model
from django.utils.translation import ugettext_lazy as _

from .. import utils

Order = get_model('order', 'Order')
RelatedOrder = get_model("oscar_support", "RelatedOrder")
TicketStatus = get_model("oscar_support", "TicketStatus")


class TicketUpdateForm(forms.ModelForm):
    message_text = forms.CharField(label=_("Message"), widget=forms.Textarea())

    class Meta:
        model = get_model("oscar_support", "Ticket")
        fields = ['message_text']


class TicketCreateForm(forms.ModelForm):

    def __init__(self, user, *args, **kwargs):
        self.user = user
        super(TicketCreateForm, self).__init__(*args, **kwargs)

    def save(self, commit=True):
        instance = super(TicketCreateForm, self).save(commit=False)

        instance.status = utils.TicketStatusGenerator.get_initial_status()
        instance.requester = self.user

        if commit:
            instance.save()
        return instance

    class Meta:
        model = get_model("oscar_support", "Ticket")
        fields = ['type', 'subject', 'body']
