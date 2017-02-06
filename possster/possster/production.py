from possster.settings import *

DEBUG = False
# ALLOWED_HOSTS = ['possster.harveyk.me', 'localhost', ]

STATIC_ROOT = '/srv/static/'

#Database
DATABASE = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': 'possster',
        'USER': 'postgres',
        'HOST': 'db',
        'PORT': 5432,
    }
}
     
