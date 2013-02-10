'''urlconf for sepal.signup'''

from django.conf.urls.defaults import url, patterns
from sepal.signup.views import *;

urlpatterns = patterns('',
    # ex: /signup/
    url(r'^$', signup),

)
