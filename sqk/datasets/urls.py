'''urlconf for sqk.datasets'''

from django.conf.urls.defaults import url, patterns
from sqk.datasets.views import *
from django.views.decorators.csrf import csrf_protect, ensure_csrf_cookie

urlpatterns = patterns('',
    # ex: /datasets/
    url(r'^$', DatasetList.as_view(), name='index'),

    # ex: /datasets/3/
    url(r'^(?P<pk>\d+)/$', ensure_csrf_cookie(DatasetDetail.as_view()),
        name='detail'),


    # ex: /datasets/new/
    url(r'^create/$', DatasetCreate.as_view(), name='create'),

    # ex: /datasets/3/edit/
    url(r'^(?P<pk>\d+)/edit/$', DatasetEdit.as_view(),
        name='edit'),

    # ex: /datasets/3/update_name
    # X-editable dataset name
    url(r'^(?P<dataset_id>\d+)/update_name/$', ensure_csrf_cookie(update_name),
        name='update_name'),

    # ex: /datasets/3/delete/
    url(r'^(?P<pk>\d+)/delete/$', DatasetDelete.as_view(),
        name='delete'),

    # ex: /datasets/instances/452/ 
    url(r'^(?P<dataset_id>\d+)/instances/(?P<pk>\d+)/$', 
        InstanceDetail.as_view(),
        name='instance_detail'),

    # ex: /datasets/instances/452/ 
    # X-editable instance label
    url(r'^/instances/(?P<instance_id>\d+)/update_label/(?P<label_name_id>\d+)$', 
        update_instance_label,
        name='update_instance_label'),

    # ex: /datasets/instances/452/delete/
    url(r'^(?P<dataset_id>\d+)/instances/(?P<pk>\d+)/delete/$', 
        InstanceDelete.as_view(),
        name='instance_delete'),

    # ex: /datasets/3/labels/create
        # ex: /datasets/new/
    url(r'^(?P<dataset_id>\d+)/labels/create/$', 
        LabelNameCreate.as_view(), name='create_label'),
)