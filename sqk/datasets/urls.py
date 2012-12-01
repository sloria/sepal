'''urlconf for sqk.datasets'''

from django.conf.urls.defaults import url, patterns
from sqk.datasets.views import DatasetList, DatasetDetail, DatasetCreate, DatasetEdit, DatasetDelete, InstanceDetail, InstanceDelete, LabelNameCreate

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

    # ex: /datasets/3/delete/
    url(r'^(?P<pk>\d+)/delete/$', DatasetDelete.as_view(),
        name='delete'),

    # TODO: /datasets/3/instances/4  <-- should capture dataset pk
    # ex: /datasets/instances/452/ 
    url(r'^(?P<dataset_id>\d+)/instances/(?P<pk>\d+)/$', 
        InstanceDetail.as_view(),
        name='instance_detail'),

    # ex: /datasets/instances/452/delete/
    url(r'^(?P<dataset_id>\d+)/instances/(?P<pk>\d+)/delete/$', 
        InstanceDelete.as_view(),
        name='instance_delete'),

    # ex: /datasets/3/labels/create
        # ex: /datasets/new/
    url(r'^(?P<dataset_id>\d)/labels/create/$', LabelNameCreate.as_view(), name='label_create'),
)