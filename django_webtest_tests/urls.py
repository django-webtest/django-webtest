
# prevent DeprecationWarning for more recent django versions
try:
    from django.conf.urls import url
except ImportError:
    from django.conf.urls.defaults import patterns, url, handler404, handler500

from django.http import HttpResponse
from django.shortcuts import render
from django.contrib.auth.views import login

from testapp_tests.views import check_password, search, set_session, \
    protected, redirect_to_protected, remove_prefix_redirect

# Uncomment the next two lines to enable the admin:
# from django.contrib import admin
# admin.autodiscover()

def simple_method_test(request):
    return HttpResponse(str(request.method))

def simple_template_render(request, template_name):
    return render(request, template_name, {
        'foo': ('a', 'b', 'c'),
        'bar': True,
        'spam': None,
    })

urlpatterns = (
    url(r'^$', simple_method_test, name='simple-method-test'),
    url(r'^template/(.*)$', simple_template_render, name='simple-template-test'),
    url(r'^check-password/$', check_password, name='check_password'),
    url(r'^search/$', search, name='search'),
    url(r'^login/$', login, name='auth_login'),
    url(r'^set-session/$', set_session, name='set_session'),
    url(r'^protected/$', protected, name='protected'),
    url(r'^redirect-to-protected/$', redirect_to_protected, name='redirect-to-protected'),
    url(r'^remove-prefix-redirect/(.*)/$', remove_prefix_redirect, name='remove-prefix-redirect'),
)
