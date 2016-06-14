#!/usr/bin/env python
import django
from django.conf import settings

TEMPLATE_CONTEXT_PROCESSORS = [
    'django.core.context_processors.debug',
    'django.core.context_processors.i18n',
    'django.core.context_processors.media',
    'django.core.context_processors.static',
    'django.core.context_processors.tz',
    'django.core.context_processors.request',
    'django.contrib.auth.context_processors.auth',
    'django.contrib.messages.context_processors.messages',
]

settings.configure(
    DEBUG = True,
    USE_TZ = True,
    INSTALLED_APPS = [
        'django.contrib.auth',
        'django.contrib.contenttypes',
        'django.contrib.sessions',
        'django.contrib.admin',
        'pandocfield',
    ],
    MIDDLEWARE_CLASSES = [
        'django.contrib.sessions.middleware.SessionMiddleware',
        'django.middleware.common.CommonMiddleware',
        'django.middleware.csrf.CsrfViewMiddleware',
        'django.contrib.auth.middleware.AuthenticationMiddleware',
        'django.contrib.auth.middleware.SessionAuthenticationMiddleware',
        'django.contrib.messages.middleware.MessageMiddleware',
        'django.middleware.clickjacking.XFrameOptionsMiddleware',
    ],
    TEMPLATE_CONTEXT_PROCESSORS = TEMPLATE_CONTEXT_PROCESSORS,
    TEMPLATES = [
        {
            'BACKEND': 'django.template.backends.django.DjangoTemplates',
            'APP_DIRS': True,
            'OPTIONS': {
                'context_processors': TEMPLATE_CONTEXT_PROCESSORS,
            },
        },
    ],
    DATABASES = {
        'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        }
    },
)

django.setup()

try:
    # Django <= 1.8
    from django.test.simple import DjangoTestSuiteRunner
    test_runner = DjangoTestSuiteRunner(verbosity=1)
except ImportError:
    # Django >= 1.8
    from django.test.runner import DiscoverRunner
    test_runner = DiscoverRunner(verbosity=1)

failures = test_runner.run_tests(['pandocfield'])
if failures:
    sys.exit(failures)
