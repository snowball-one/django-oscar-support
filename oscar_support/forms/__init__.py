from django import forms
from django.conf import settings
from django.db.models import get_model
from django.utils.translation import ugettext_lazy as _

from .. import defaults

Order = get_model('order', 'Order')
RelatedOrder = get_model("oscar_support", "RelatedOrder")
TicketStatus = get_model("oscar_support", "TicketStatus")

SUPPORT_INITIAL_STATUS = getattr(
    settings,
    "SUPPORT_INITIAL_STATUS",
    defaults.SUPPORT_INITIAL_STATUS
)


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

        initial_status, __ = TicketStatus.objects.get_or_create(
            name=SUPPORT_INITIAL_STATUS
        )
        instance.status = initial_status
        instance.requester = self.user

        if commit:
            instance.save()
        return instance

    class Meta:
        model = get_model("oscar_support", "Ticket")
        fields = ['type', 'subject', 'body']
