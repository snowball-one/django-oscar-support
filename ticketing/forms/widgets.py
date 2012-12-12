from django.forms.util import flatatt
from django.template import loader, Context
from django.utils.encoding import force_unicode
from django.utils.html import conditional_escape
from django.template.loader import render_to_string
from django.forms.widgets import Widget, RadioInput, RadioFieldRenderer


class AutoCompleteWiget(Widget):

    def __init__(self, url, user_field=None, *args, **kwargs):
        self.url = url
        self.user_field = user_field
        super(AutoCompleteWiget, self).__init__(*args, **kwargs)

    def render(self, name, value, attrs=None):
        if value is None:
            value = []
        tmpl = loader.get_template('ticketing/widgets/autocomplete_widget.html')
        return tmpl.render(Context({
            'name': name,
            'url': self.url,
            'user_field': self.user_field,
        }))


class CustomRadioInput(RadioInput):
    template_name = 'ticketing/partials/custom_radio_select.html'

    def render(self, name=None, value=None, attrs=None, choices=()):
        name = name or self.name
        value = value or self.value
        attrs = attrs or self.attrs

        if 'id' in self.attrs:
            self.attrs['id'] = '%s_%s' % (self.attrs['id'], self.index)

        print self.attrs['id']
        if 'id' in self.attrs:
            label_for = ' for="%s"' % self.attrs['id']
        else:
            label_for = ''
        print label_for 

        choice_label = conditional_escape(force_unicode(self.choice_label))
        return render_to_string(self.template_name, Context({
            'attrs': flatatt(self.attrs),
            'checked': self.is_checked(),
            'name': self.name,
            'value': self.choice_value,
            'label_for': label_for,
            'choice_label': choice_label,
        }))


class CustomRadioFieldRenderer(RadioFieldRenderer):

    def __iter__(self):
        for i, choice in enumerate(self.choices):
            yield CustomRadioInput(self.name, self.value, self.attrs.copy(), choice, i)

    def __getitem__(self, idx):
        choice = self.choices[idx] # Let the IndexError propogate
        return CustomRadioInput(self.name, self.value, self.attrs.copy(), choice, idx)
