"""urlconf for celerytest"""

from django.conf.urls.defaults import url, patterns
from sqk.celerytest import views

urlpatterns = patterns('',
    url(r'', views.test_celery, name='test_celery'),
    )