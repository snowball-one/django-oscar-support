from django.db.models import get_model
from django.utils.translation import ugettext_lazy as _

SUPPORT_INITIAL_STATUS = _("New")
SUPPORT_INITIAL_STATUS_SLUG = "new"

SUPPORT_RESOLVED_STATUS = _("Resolved")
SUPPORT_RESOLVED_STATUS_SLUG = "resolved"

TicketStatus = get_model("oscar_support", "TicketStatus")


# Setting defaults for the REST API provided by django-rest-framework
# for security reasons we only enable session-based authentication and
# JSON formatting. This can be overwritten in you own settings file. For more
# details on the DRF settings checkout http://django-rest-framework.org
REST_FRAMEWORK = {
    'DEFAULT_PERMISSION_CLASSES': (
        'rest_framework.permissions.IsAuthenticated',
    ),
    'DEFAULT_AUTHENTICATION_CLASSES': (
        'rest_framework.authentication.SessionAuthentication',
    ),
    'DEFAULT_RENDERER_CLASSES': (
        'rest_framework.renderers.JSONRenderer',
    )
}


def get_ticket_initial_status():
    try:
        initial_status = TicketStatus.objects.get(
            slug=SUPPORT_INITIAL_STATUS_SLUG
        )
    except TicketStatus.DoesNotExist:
        initial_status = TicketStatus.objects.create(
            slug=SUPPORT_INITIAL_STATUS_SLUG,
            name=SUPPORT_INITIAL_STATUS
        )
    return initial_status


def get_ticket_resolved_status():
    try:
        resolved_status = TicketStatus.objects.get(
            slug=SUPPORT_RESOLVED_STATUS_SLUG
        )
    except TicketStatus.DoesNotExist:
        resolved_status = TicketStatus.objects.create(
            slug=SUPPORT_RESOLVED_STATUS_SLUG,
            name=SUPPORT_RESOLVED_STATUS
        )
    return resolved_status
