from django import forms
from django.conf import settings
from django.db.models import get_model


class TicketCreateForm(forms.ModelForm):

    class Meta:
        model = get_model('ticketing', 'Ticket')
        exclude = ['number', 'subticket_number', 'parent',
                   'date_created', 'date_updated']
        widgets = {
            'status': forms.HiddenInput(),
        }
