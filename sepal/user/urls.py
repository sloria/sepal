# The views used below are normally mapped in django.contrib.admin.urls.py
# This URLs file is used to provide a reliable view deployment for test purposes.
# It is also provided as a convenience to those who want to deploy these URLs
# elsewhere.

from django.conf.urls import patterns, url

urlpatterns = patterns('',
    url(r'^login/$', 'django.contrib.auth.views.login', {'template_name': 'base/home.html'}, name='login'),
    url(r'^logout/$', 'django.contrib.auth.views.logout', {'template_name': 'base/home.html'}, name='logout'),
    url(r'^password_change/$', 'django.contrib.auth.views.password_change', {'template_name': 'user/password_change_form.html', 'post_change_redirect': '/user/password_change/done/'}, name='password_change'),
    url(r'^password_change/done/$', 'django.contrib.auth.views.password_change_done', {'template_name': 'user/password_change_done.html'}, name='password_change_done'),
    url(r'^password_reset/$', 'django.contrib.auth.views.password_reset', {'template_name': 'user/password_reset_form.html', 'post_reset_redirect': 'user/password_reset/done/'}, name='password_reset'),
    url(r'^password_reset/done/$', 'django.contrib.auth.views.password_reset_done', {'template_name': 'user/password_reset_done.html'}, name='password_reset_done'),
    url(r'^reset/(?P<uidb36>[0-9A-Za-z]{1,13})-(?P<token>[0-9A-Za-z]{1,13}-[0-9A-Za-z]{1,20})/$',
        'django.contrib.auth.views.password_reset_confirm', { 'post_reset_redirect': '/user/reset/done/' },
        name='password_reset_confirm'),
    url(r'^reset/done/$', 'django.contrib.auth.views.password_reset_complete', {'template_name': 'user/password_reset_complete.html'}, name='password_reset_complete'),
)
