'''urlconf for sepal.datasets'''

from django.conf.urls.defaults import url, patterns
from sepal.datasets.views import *

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

    # ex: /datasets/3/upload/
    url(r'^(?P<pk>\d+)/upload/$', multiple_uploader,
        name='upload'),

    # ex: /datasets/3/delete/
    url(r'^(?P<pk>\d+)/delete/$', delete_dataset,
        name='delete_dataset'),

    # ex: /datasets/3/delete_instances/
    url(r'^(?P<pk>\d+)/delete_instances/$', delete_instances,
        name='delete_instances'),
    
    # ex: /datasets/3/instances/452/delete/
    url(r'^(?P<dataset_id>\d+)/instances/(?P<pk>\d+)/delete/$',
        SingleInstanceDelete.as_view(),
        name='single_instance_delete'),


    # ex: /datasets/3/update_instances_labels/
    url(r'^(?P<dataset_id>\d+)/update_instances_labels/(?P<label_name_id>\d+)$',
        update_instances_labels,
        name='update_instances_labels'),

    # ex: /datasets/3/load_data
    url(r'^(?P<pk>\d+)/load_data/$', load_data,
        name='load_data'),
)

# URLconfs for X-editable updating
urlpatterns += patterns('',
    # ex: /datasets/3/update_name
    # X-editable dataset name
    url(r'^(?P<dataset_id>\d+)/update_name/$', update_name,
        name='update_name'),

    # ex: /datasets/3/update_description
    # X-editable dataset name
    url(r'^(?P<dataset_id>\d+)/update_description/$', update_description,
        name='update_description'),

    # ex: /datasets/3/update_description
    # X-editable dataset name
    url(r'^(?P<dataset_id>\d+)/update_species/$', update_species,
        name='update_species'),

    # ex: /datasets/instances/452/update_label/4
    # X-editable instance label
    url(r'^(?P<dataset_id>\d+)/instances/(?P<instance_id>\d+)/update_label/(?P<label_name_id>\d+)$',
        update_instance_label,
        name='update_instance_label'),

    # ex: /datasets/3/update_label/5
    # X-editable label name
    url(r'^(?P<dataset_id>\d+)/update_label/(?P<label_name_id>\d+)$',
        update_label_name,
        name='update_label_name'),
)
