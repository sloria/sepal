'''urlconf for sqk.datasets'''

from django.conf.urls.defaults import url, patterns
from django.views.generic import ListView
from sqk.datasets import views

urlpatterns = patterns('',
    # ex: /datasets/
    url(r'^$', views.index, name='index'),
        
    )