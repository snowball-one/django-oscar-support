from django import forms
from django.db.models import get_model
from django.utils.translation import ugettext_lazy as _

CommunicationEventType = get_model('customer', 'CommunicationEventType')


class TicketCreateForm(forms.ModelForm):

    class Meta:
        model = get_model('ticketing', 'Ticket')
        exclude = ['number', 'subticket_number', 'parent',
                   'date_created', 'date_updated']
        widgets = {
            'status': forms.HiddenInput(),
        }


class TicketUpdateForm(forms.ModelForm):
    MESSAGE_CHOICES = (
        ('message', _("Public reply")),
        ('note', _("Internal note")),
    )
    message_type = forms.ChoiceField(widget=forms.RadioSelect(),
                                     choices=MESSAGE_CHOICES,
                                     label=_("Message type"),
                                     initial='message', required=False)
    message_text = forms.CharField(widget=forms.Textarea(attrs={'rows': 5}),
                                   label=_("Message text"), required=False)

    message_template = forms.ChoiceField(label=_("Template"), required=False)

    def __init__(self, *args, **kwargs):
        super(TicketUpdateForm, self).__init__(*args, **kwargs)

        template_choices = [('', _("Please select a template"))]
        for event_type in CommunicationEventType.objects.all():
            template_choices.append((event_type.id, event_type.name,))

        self.fields['message_template'].choices = template_choices

    def get_property_fields(self):
        for field in self:
            if not field.name.startswith('message'):
                yield field

    def get_message_fields(self):
        for field in self:
            if field.name.startswith('message'):
                yield field

    class Meta:
        model = get_model('ticketing', 'Ticket')
        exclude = ['number', 'subticket_number', 'parent', 'body', 'subject',
                   'date_created', 'date_updated', 'requester', 'is_internal']
        widgets = {
            'status': forms.HiddenInput(),
        }
