""" This file is here to register objects with the admin site. """
from django.contrib import admin

from .models import Article

admin.site.register(Article)
