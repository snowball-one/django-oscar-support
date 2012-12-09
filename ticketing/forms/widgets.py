from django.forms.widgets import Widget
from django.template import loader, Context


class AutoCompleteWiget(Widget):

    def __init__(self, url, *args, **kwargs):
        self.url = url
        super(AutoCompleteWiget, self).__init__(*args, **kwargs)

    def render(self, name, value, attrs=None):
        if value is None:
            value = []
        tmpl = loader.get_template('ticketing/widgets/autocomplete_widget.html')
        return tmpl.render(Context({'name': name, 'url': self.url}))
