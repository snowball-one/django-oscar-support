from django.conf import settings

__version__ = (0, 0, 1, 'dev', 0)

TICKETING_INITIAL_STATUS = getattr(settings, "TICKETING_INITIAL_STATUS", "New")
