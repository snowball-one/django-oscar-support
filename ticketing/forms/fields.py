from django.db import models
from django.forms.fields import CharField
from django.core.exceptions import ValidationError
from django.utils.translation import ugettext_lazy as _

from ticketing.forms.widgets import AutoCompleteWiget


class AutoCompleteField(CharField):
    __metaclass__ = models.SubfieldBase

    def __init__(self, model, url=None, user_field=None, *args, **kwargs):
        self.model = model
        self.url = url
        self.user_field = user_field
        super(AutoCompleteField, self).__init__(*args, **kwargs)

        if not self.url:
            self.url = '/api/v1/%s/search/' % self.model._meta.module_name
        self.widget = AutoCompleteWiget(url=url, user_field=self.user_field)

    def prepare_value(self, value):
        if hasattr(value, '_meta'):
            return value.pk
        return super(AutoCompleteField, self).prepare_value(value)

    def to_python(self, value):
        value = super(AutoCompleteField, self).to_python(value)
        if not value:
            return None

        try:
            value = self.model.objects.get(id=value)
        except (self.model.DoesNotExist, self.model.MultipleObjectsReturned):
            raise ValidationError(
                _("no matching query for model %s") % self.model.__class__
            )
        return value
