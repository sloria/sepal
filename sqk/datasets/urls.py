'''urlconf for sqk.datasets'''

from django.conf.urls.defaults import url, patterns
from django.views.generic import ListView, DetailView
from sqk.datasets import views
from sqk.datasets.models import Dataset

urlpatterns = patterns('',
    # ex: /datasets/
    url(r'^$', ListView.as_view(
            queryset=Dataset.objects.all(),
            context_object_name='all_datasets',
            template_name='datasets/index.html'
            ), 
        name='index'),

    # ex: /datasets/
    url(r'^/(?P<pk>\d+)/$', DetailView.as_view(
            model=Dataset,
            context_object_name='dataset',
            template_name='datasets/detail.html'))
    )