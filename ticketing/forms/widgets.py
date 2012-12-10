from django.forms.widgets import Widget
from django.template import loader, Context


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
