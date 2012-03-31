# -*- coding: utf-8 -*-
from django.contrib.auth.middleware import RemoteUserMiddleware
from django.core.exceptions import ImproperlyConfigured
from django.core import signals
from django.db import close_connection
from django.contrib import auth

class WebtestUserMiddleware(RemoteUserMiddleware):
    """
    Middleware for utilizing django-webtest simplified auth
    ('user' arg for self.app.post and self.app.get).

    Mostly copied from RemoteUserMiddleware, but the auth backend is changed
    (by changing ``auth.authenticate`` arguments) in order to keep
    RemoteUser backend untouched during django-webtest auth.
    """

    header = "WEBTEST_USER"

    def process_request(self, request):
        # AuthenticationMiddleware is required so that request.user exists.
        if not hasattr(request, 'user'):
            raise ImproperlyConfigured(
                "The django-webtest auth middleware requires the "
                "'django.contrib.auth.middleware.AuthenticationMiddleware' "
                "to be installed. Add it to your MIDDLEWARE_CLASSES setting "
                "or disable django-webtest auth support "
                "by setting 'setup_auth' property of your WebTest subclass "
                "to False."
            )
        try:
            username = request.META[self.header]
        except KeyError:
            # If specified header doesn't exist then return (leaving
            # request.user set to AnonymousUser by the
            # AuthenticationMiddleware).
            return
        # If the user is already authenticated and that user is the user we are
        # getting passed in the headers, then the correct user is already
        # persisted in the session and we don't need to continue.
        if request.user.is_authenticated():
            if request.user.username == self.clean_username(username, request):
                return
        # We are seeing this user for the first time in this session, attempt
        # to authenticate the user.
        user = auth.authenticate(django_webtest_user=username)
        if user:
            # User is valid.  Set request.user and persist user in the session
            # by logging the user in.
            request.user = user
            auth.login(request, user)


class DisableCSRFCheckMiddleware(object):
    def process_request(self, request):
        request._dont_enforce_csrf_checks = True


class DjangoWsgiFix(object):
    """Django closes the database connection after every request;
    this breaks the use of transactions in your tests. This wraps
    around Django's WSGI interface and will disable the critical
    signal handler for every request served.

    Note that we really do need to do this individually a every
    request, not just once when our WSGI hook is installed, since
    Django's own test client does the same thing; it would reinstall
    the signal handler if used in combination with us.

    From django-test-utils.
    Note: that's WSGI middleware, not django's.
    """
    def __init__(self, app):
        self.app = app

    def __call__(self, environ, start_response):
        signals.request_finished.disconnect(close_connection)
        try:
            return self.app(environ, start_response)
        finally:
            signals.request_finished.connect(close_connection)
