import os
import sys

from django.conf import settings

location = lambda x: os.path.join(
    os.path.dirname(os.path.realpath(__file__)), x
)
sandbox = lambda x: location("sandbox/%s" % x)

sys.path.insert(0, location('sandbox'))

from oscar import get_core_apps
from oscar import OSCAR_MAIN_TEMPLATE_DIR
from oscar.defaults import OSCAR_SETTINGS



def pytest_configure():
    if not settings.configured:
        settings.configure(
            DATABASES={
                'default': {
                    'ENGINE': 'django.db.backends.sqlite3',
                    'NAME': ':memory:',
                }
            },
            MEDIA_ROOT=sandbox('public/media'),
            MEDIA_URL='/media/',
            STATIC_URL='/static/',
            STATICFILES_DIRS=[
                sandbox('static/')
            ],
            STATIC_ROOT=sandbox('public'),
            STATICFILES_FINDERS=(
                'django.contrib.staticfiles.finders.FileSystemFinder',
                'django.contrib.staticfiles.finders.AppDirectoriesFinder',
                'compressor.finders.CompressorFinder',
            ),
            TEMPLATE_LOADERS=(
                'django.template.loaders.filesystem.Loader',
                'django.template.loaders.app_directories.Loader',
            ),
            TEMPLATE_CONTEXT_PROCESSORS = (
                "django.contrib.auth.context_processors.auth",
                "django.core.context_processors.request",
                "django.core.context_processors.debug",
                "django.core.context_processors.i18n",
                "django.core.context_processors.media",
                "django.core.context_processors.static",
                "django.contrib.messages.context_processors.messages",
                'oscar.apps.search.context_processors.search_form',
                'oscar.apps.promotions.context_processors.promotions',
                'oscar.apps.checkout.context_processors.checkout',
                'oscar.apps.customer.notifications.context_processors.notifications',
                'oscar.core.context_processors.metadata',
            ),
            MIDDLEWARE_CLASSES=(
                'django.middleware.common.CommonMiddleware',
                'django.contrib.sessions.middleware.SessionMiddleware',
                'django.middleware.csrf.CsrfViewMiddleware',
                'django.contrib.auth.middleware.AuthenticationMiddleware',
                'django.contrib.messages.middleware.MessageMiddleware',
                'django.contrib.flatpages.middleware.FlatpageFallbackMiddleware',
                'oscar.apps.basket.middleware.BasketMiddleware',
            ),
            ROOT_URLCONF='sandbox.sandbox.urls',
            TEMPLATE_DIRS=[
                sandbox('templates'),
                OSCAR_MAIN_TEMPLATE_DIR,
            ],
            INSTALLED_APPS=[
                'django.contrib.auth',
                'django.contrib.contenttypes',
                'django.contrib.sessions',
                'django.contrib.sites',
                'django.contrib.messages',
                'django.contrib.staticfiles',
                'django.contrib.admin',
                'haystack',
                'compressor',
                'south',

                'oscar_support',
            ] + get_core_apps(),
            AUTHENTICATION_BACKENDS=(
                'django.contrib.auth.backends.ModelBackend',
            ),
            COMPRESS_ENABLED=True,
            COMPRESS_OFFLINE=False,
            COMPRESS_PRECOMPILERS=(
                ('text/less', 'lessc {infile} {outfile}'),
            ),
            LOGIN_REDIRECT_URL='/accounts/',
            APPEND_SLASH=True,
            SITE_ID=1,
            HAYSTACK_CONNECTIONS = {
                'default': {
                    'ENGINE': 'haystack.backends.simple_backend.SimpleEngine',
                },
            },
            **OSCAR_SETTINGS
        )
