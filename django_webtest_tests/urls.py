import django
from django.http import HttpResponse
from django.shortcuts import render

from testapp_tests.views import check_password, search, set_session, \
    protected, redirect_to_protected, remove_prefix_redirect, cookie_test


major_version = int(django.__version__[0])

if major_version >= 4:
    from django.urls import re_path
else:
    try:
        from django.conf.urls import url
    except ImportError:
        from django.conf.urls.defaults import url


try:
    from django.contrib.auth.views import login
except ImportError:
    # django 2+
    from django.contrib.auth.views import LoginView
    login = LoginView.as_view()


def simple_method_test(request):
    return HttpResponse(str(request.method))


def simple_template_render(request, template_name):
    return render(request, template_name, {
        'user': request.user,
        'foo': ('a', 'b', 'c'),
        'bar': True,
        'spam': None,
    })


if major_version >= 4:
    urlpatterns = (
        re_path(r'$', simple_method_test, name='simple-method-test'),
        re_path(r'template/(.*)$', simple_template_render,
                name='simple-template-test'),
        re_path(r'check-password/$', check_password, name='check_password'),
        re_path(r'search/$', search, name='search'),
        re_path(r'login/$', login, name='auth_login'),
        re_path(r'set-session/$', set_session, name='set_session'),
        re_path(r'protected/$', protected, name='protected'),
        re_path(r'redirect-to-protected/$',
                redirect_to_protected, name='redirect-to-protected'),
        re_path(r'remove-prefix-redirect/(.*)/$',
                remove_prefix_redirect, name='remove-prefix-redirect'),
        re_path(r'cookie-test/$', cookie_test, name='cookie_test'),
    )
else:
    urlpatterns = (
        url(r'^$', simple_method_test, name='simple-method-test'),
        url(r'^template/(.*)$', simple_template_render,
            name='simple-template-test'),
        url(r'^check-password/$', check_password, name='check_password'),
        url(r'^search/$', search, name='search'),
        url(r'^login/$', login, name='auth_login'),
        url(r'^set-session/$', set_session, name='set_session'),
        url(r'^protected/$', protected, name='protected'),
        url(r'^redirect-to-protected/$',
            redirect_to_protected, name='redirect-to-protected'),
        url(r'^remove-prefix-redirect/(.*)/$',
            remove_prefix_redirect, name='remove-prefix-redirect'),
        url(r'^cookie-test/$', cookie_test, name='cookie_test'),
    )
