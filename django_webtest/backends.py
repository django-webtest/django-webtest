from __future__ import absolute_import
from django.contrib.auth.backends import RemoteUserBackend
from .compat import from_wsgi_safe_string


class WebtestUserBackend(RemoteUserBackend):
    """ Auth backend for django-webtest auth system """

    def authenticate(self, request, django_webtest_user):
        return super(WebtestUserBackend, self).authenticate(
            request, django_webtest_user)

    def clean_username(self, username):
        return from_wsgi_safe_string(username)
