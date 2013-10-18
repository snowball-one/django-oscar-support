SUPPORT_INITIAL_STATUS = "New"
SUPPORT_RESOLVED_STATUS = "Resolved"

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
