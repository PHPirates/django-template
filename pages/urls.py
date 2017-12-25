""" url configuration """
from django.conf.urls import url

from . import views

urlpatterns = [
    # When not using a class, use line below
    # url(r'^$', views.index, name='index'),
    url(r'^$', views.IndexView.as_view(), name='index'),
]
