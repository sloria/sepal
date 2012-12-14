'''urlconf for sqk.datasets'''

from django.conf.urls.defaults import url, patterns
from sqk.datasets.views import *

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

    # ex: /datasets/instances/452/ 
    url(r'^(?P<dataset_id>\d+)/instances/(?P<pk>\d+)\.?(?P<format>\w+)?$', 
        InstanceDetail.as_view(),
        name='instance_detail'),

    # ex: /datasets/instances/452/ready.json
    url(r'^(?P<dataset_id>\d+)/instances/(?P<pk>\d+)/ready.json$', 
        InstanceDetail.as_view(),
        name='instance_ready'),

    # ex: /datasets/instances/452/row/
    url(r'^(?P<dataset_id>\d+)/instances/(?P<pk>\d+)/row$', 
        InstanceRow.as_view(),
        name='instance_row'),

    # ex: /datasets/instances/452/delete/
    url(r'^(?P<dataset_id>\d+)/instances/(?P<pk>\d+)/delete/$', 
        InstanceDelete.as_view(),
        name='instance_delete'),

    # ex: /datasets/3/labels/create
        # ex: /datasets/new/
    url(r'^(?P<dataset_id>\d+)/labels/create/$', 
        LabelNameCreate.as_view(), name='create_label'),
)

# URLconfs for X-editable updating
urlpatterns += patterns('',
    # ex: /datasets/3/update_name
    # X-editable dataset name
    url(r'^(?P<dataset_id>\d+)/update_name/$', update_name,
        name='update_name'),
    
    # ex: /datasets/instances/452/update_label/4
    # X-editable instance label
    url(r'^/instances/(?P<instance_id>\d+)/update_label/(?P<label_name_id>\d+)$', 
        update_instance_label,
        name='update_instance_label'),

    # ex: /datasets/3/update_label/5
    # X-editable label name
    url(r'^(?P<dataset_id>\d+)/update_label/(?P<label_name_id>\d+)$', 
        update_label_name,
        name='update_label_name'),
)

