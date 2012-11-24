'''urlconf for sqk.datasets'''

from django.conf.urls.defaults import url, patterns
from sqk.datasets.views import DatasetList, DatasetDetail, DatasetCreate, DatasetEdit

urlpatterns = patterns('',
    # ex: /datasets/
    url(r'^$', DatasetList.as_view(), name='index'),

    # ex: /datasets/3/
    url(r'^(?P<pk>\d+)/$', DatasetDetail.as_view(),
        name='detail'),

    # ex: /datasets/new/
    url(r'^create/$', DatasetCreate.as_view(), name='create'),

    # ex: /datasets/3/edit/
    url(r'^(?P<pk>\d+)/edit/$', DatasetEdit.as_view(),
        name='edit'),
)