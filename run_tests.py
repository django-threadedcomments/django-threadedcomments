#!/usr/bin/env python
import sys
from django.conf import settings, global_settings as default_settings
from django.core.management import execute_from_command_line

if not settings.configured:
    settings.configure(
        DATABASES={
            'default': {
                'ENGINE': 'django.db.backends.sqlite3',
            }
        },
        TEMPLATE_LOADERS=(
            'django.template.loaders.app_directories.Loader',
        ),
        TEMPLATE_CONTEXT_PROCESSORS=default_settings.TEMPLATE_CONTEXT_PROCESSORS + (  # noqa
            'django.core.context_processors.request',
        ),
        INSTALLED_APPS=(
            'django.contrib.sessions',
            'django.contrib.auth',
            'django.contrib.contenttypes',
            'django.contrib.sites',
            'threadedcomments',
            'threadedcomments.tests',
            'django_nose',
        ),
        MIDDLEWARE_CLASSES=(
            'django.contrib.sessions.middleware.SessionMiddleware',
            'django.contrib.auth.middleware.AuthenticationMiddleware',
        ),
        ROOT_URLCONF='threadedcomments.urls',
        TEST_RUNNER='django_nose.NoseTestSuiteRunner',
        SITE_ID=1,
    )


def runtests():
    argv = sys.argv[:1] + ['test', 'threadedcomments', '--traceback'] + sys.argv[1:]  # noqa
    execute_from_command_line(argv)

if __name__ == '__main__':
    runtests()
