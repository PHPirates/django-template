"""
SECURITY WARNING Keep these settings secret, they are for production.
"""

from mysite.settings.base import *

SECRET_KEY = 'mykey'

STATIC_ROOT = os.path.join(BASE_DIR, "static")

DEBUG = False

# Settings for database on deployment server
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': 'django_template_db',
        'USER': 'django_template',
        'PASSWORD': 'databasepassword',
        'HOST': 'server ip address',
        'PORT': '5432',
    }
}
