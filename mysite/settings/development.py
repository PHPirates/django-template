""" Settings for development purposes. """
from mysite.settings.base import *

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = '(mk5n7s)#kozir!hh7crys^qj%b-gs@nt@9rk*@x!8dg8j9o=='

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

# Database
# https://docs.djangoproject.com/en/1.11/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': 'django_template_db',
        'USER': 'django_template',
        'PASSWORD': 'IcoXGoOqJ',
        'HOST': '127.0.0.1',
        'PORT': '5432',
    }
}
