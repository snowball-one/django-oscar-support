from django import forms
from django.db.models import get_model
from django.core.urlresolvers import reverse_lazy
from django.utils.translation import ugettext_lazy as _

from oscar.core.compat import get_user_model

from ..forms.widgets import AutoCompleteWidget, CustomRadioFieldRenderer

User = get_user_model()
Ticket = get_model('oscar_support', 'Ticket')
Message = get_model('oscar_support', 'Message')
CommunicationEventType = get_model('customer', 'CommunicationEventType')


REQUESTER_FIELDS = ['requester', 'is_internal']
MESSAGE_FIELDS = ['subject', 'body']


class TicketCreateForm(forms.ModelForm):
    requester = forms.IntegerField(
        widget=AutoCompleteWidget(
            url=reverse_lazy('support-api:customer-list')
        )
    )
    assignee = forms.IntegerField(
        widget=AutoCompleteWidget(
            url=reverse_lazy('support-api:agent-list'),
        ),
        required=False,
    )

    def get_message_fields(self):
        for field in self:
            if field.name in MESSAGE_FIELDS:
                yield field

    def get_property_fields(self):
        for field in self:
            if field.name not in REQUESTER_FIELDS + MESSAGE_FIELDS:
                yield field

    def clean_requester(self):
        requester_id = self.cleaned_data.get('requester')
        try:
            requester = User.objects.get(id=requester_id)
        except User.DoesNotExist:
            raise forms.ValidationError("Invalid user specified")
        return requester

    def clean_assignee(self):
        assignee_id = self.cleaned_data.get('assignee')
        # The assignee is not mandatory so if it is empty, we just ignore it
        if not assignee_id:
            return assignee_id
        try:
            assignee = User.objects.get(id=assignee_id, is_staff=True)
        except User.DoesNotExist:
            raise forms.ValidationError("Invalid user specified")
        return assignee

    class Meta:
        model = get_model('oscar_support', 'Ticket')
        fields = REQUESTER_FIELDS + [
            'status',
            'priority', 'type',
            'assigned_group', 'assignee',
        ] + MESSAGE_FIELDS
        widgets = {'status': forms.HiddenInput()}


class TicketUpdateForm(forms.ModelForm):
    message_type = forms.ChoiceField(
        widget=forms.RadioSelect(renderer=CustomRadioFieldRenderer),
        choices=Message.MESSAGE_TYPES,
        label=_("Message type"),
        initial=Message.PUBLIC,
    )
    message_text = forms.CharField(
        widget=forms.Textarea(attrs={'rows': 5}),
        label=_("Message text"),
        required=False
    )
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
        model = get_model('oscar_support', 'Ticket')
        fields = ['status', 'message_type', 'message_text']
        widgets = {
            'status': forms.HiddenInput(),
        }


class RequesterCreateForm(forms.ModelForm):
    first_name = forms.CharField(max_length=255)
    last_name = forms.CharField(max_length=255)
    email = forms.EmailField()

    class Meta:
        model = get_model('auth', 'User')
        fields = ['first_name', 'last_name', 'email']
