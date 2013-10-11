from django import forms
from django.db.models import get_model
from django.utils.translation import ugettext_lazy as _

from ..forms.fields import AutoCompleteField
from ..forms.widgets import CustomRadioFieldRenderer

User = get_model('auth', 'User')
Message = get_model('oscar_support', 'Message')
CommunicationEventType = get_model('customer', 'CommunicationEventType')


class TicketCreateForm(forms.ModelForm):
    requester = AutoCompleteField(model=User, url='/api/v1/user/search/')
    assignee = AutoCompleteField(
        model=User,
        url='/api/v1/agent/search/',
        required=False
    )

    def get_requester_fields(self):
        for field in self:
            if field.name.startswith('requester'):
                yield field

    def get_message_fields(self):
        for field in self:
            if field.name in ['body', 'subject']:
                yield field

    def get_property_fields(self):
        for field in self:
            if (field.name not in ['body', 'subject']
               and not field.name.startswith('requester')):
                yield field

    class Meta:
        model = get_model('oscar_support', 'Ticket')
        exclude = ['number', 'subticket_number', 'parent',
                   'date_created', 'date_updated']
        widgets = {
            'status': forms.HiddenInput(),
        }


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


class RelatedOrderForm(forms.ModelForm):
    order = AutoCompleteField(
        model=get_model('order', 'Order'),
        url='/api/v1/order/search/'
    )

    class Meta:
        model = get_model('oscar_support', 'RelatedOrder')


class RelatedOrderLineForm(forms.ModelForm):
    line = AutoCompleteField(
        model=get_model('order', 'Line'),
        url='/api/v1/line/search/'
    )

    class Meta:
        model = get_model('oscar_support', 'RelatedOrderLine')


class RelatedProductForm(forms.ModelForm):
    product = AutoCompleteField(
        model=get_model('catalogue', 'Product'),
        url='/api/v1/product/search/'
    )

    class Meta:
        model = get_model('oscar_support', 'RelatedProduct')
