from django.db import models
from django.utils.timezone import now as utc_now
from django.utils.translation import ugettext_lazy as _


class ModificationTrackingMixin(models.Model):
    date_created = models.DateTimeField(_("Created"))
    date_updated = models.DateTimeField(_("Last modified"))

    def save(self, *args, **kwargs):
        if not self.date_created:
            self.date_created = utc_now()
        self.date_updated = utc_now()
        super(ModificationTrackingMixin, self).save(*args, **kwargs)

    class Meta:
        abstract = True
