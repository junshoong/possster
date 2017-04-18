from possster.settings import *

DEBUG = False
ALLOWED_HOSTS = ['possster.junshoong.net','52.79.137.232', ]

STATIC_ROOT = '/srv/static/'
MEDIA_ROOT = '/srv/media/'

# Database
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': 'postgres',
        'USER': 'postgres',
        'PASSWORD': '',
        'HOST': 'db',
        'PORT': 5432,
    }
}
