import os
import sys
import django

PROJECT_ROOT = os.path.dirname(os.path.abspath(__file__))
join = lambda p: os.path.abspath(os.path.join(PROJECT_ROOT, p))

# TODO configure pytest testpaths instead of doing this
sys.path.insert(0, join('..'))

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': join('db.sqlite'),
        'USER': '',
        'PASSWORD': '',
        'HOST': '',
        'PORT': '',
    }
}

if os.environ.get('USE_POSTGRES'):
    DATABASES['default']['ENGINE'] = 'django.db.backends.postgresql_psycopg2'
    DATABASES['default']['NAME'] = 'django_webtest_tests'


SITE_ID = 1
ROOT_URLCONF = 'urls'
SECRET_KEY = '5mcs97ar-(nnxhfkx0%^+0^sr!e(ax=x$2-!8dqy25ff-l1*a='
DEBUG = False

USE_I18N = True
USE_L10N = True
TIME_ZONE = 'America/Chicago'
LANGUAGE_CODE = 'en-us'

MEDIA_ROOT = join('media')
MEDIA_URL = '/media/'
STATIC_URL = '/static/'
LOGIN_REDIRECT_URL = '/template/index.html'


TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [],
        'APP_DIRS': True,
        'OPTIONS': {
            'debug': DEBUG,
            'context_processors': [
                'django.contrib.auth.context_processors.auth',
                'django.template.context_processors.debug',
                'django.template.context_processors.i18n',
                'django.template.context_processors.media',
                'django.template.context_processors.static',
                'django.template.context_processors.tz',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]


if django.VERSION < (1, 10):
    TEMPLATE_DEBUG = DEBUG

    TEMPLATE_LOADERS = (
        'django.template.loaders.filesystem.Loader',
        'django.template.loaders.app_directories.Loader',
    )

    TEMPLATE_DIRS = (
        join('templates'),
    )


MIDDLEWARE = (
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'testapp_tests.middleware.UserMiddleware',
)

if django.VERSION < (1, 10):
    MIDDLEWARE_CLASSES = MIDDLEWARE
    del MIDDLEWARE


INSTALLED_APPS = (
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.sites',
    'django.contrib.messages',
    'django_webtest',
    'django_webtest_tests',
    'django_webtest_tests.testapp_tests',
)
