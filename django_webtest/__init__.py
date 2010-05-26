#coding: utf-8
from django.conf import settings
from django.core.handlers.wsgi import WSGIHandler
from django.core.servers.basehttp import AdminMediaHandler
from django.db import close_connection
from django.core import signals
from django.test import TestCase
from webtest import TestApp, TestRequest


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
    """
    def __init__(self, app):
        self.app = app

    def __call__(self, environ, start_response):
        signals.request_finished.disconnect(close_connection)
        try:
            return self.app(environ, start_response)
        finally:
            signals.request_finished.connect(close_connection)


class DjangoTestApp(TestApp):

    def __init__(self, extra_environ=None, relative_to=None):
        app = DjangoWsgiFix(AdminMediaHandler(WSGIHandler()))
        super(DjangoTestApp, self).__init__(app, extra_environ, relative_to)


    def get(self, url, params=None, headers=None, extra_environ=None,
            status=None, expect_errors=False, user=None):
        if user:
            extra_environ = extra_environ or {}
            extra_environ['REMOTE_USER'] = user
        return super(DjangoTestApp, self).get(url, params, headers, extra_environ,
                                              status, expect_errors)


    def post(self, url, params=None, headers=None, extra_environ=None,
             status=None, upload_files=None, expect_errors=False,
             content_type=None, user=None):
        if user:
            extra_environ = extra_environ or {}
            extra_environ['REMOTE_USER'] = user
        return super(DjangoTestApp, self).post(url, params, headers,
                                               extra_environ, status,
                                               upload_files, expect_errors,
                                               content_type)


class WebTest(TestCase):

    extra_environ = {}

    def _patch_settings(self):
        ''' Patch settings to add support for REMOTE_USER authorization '''
        self._MIDDLEWARE_CLASSES = settings.MIDDLEWARE_CLASSES[:]
        self._AUTHENTICATION_BACKENDS = settings.AUTHENTICATION_BACKENDS[:]

        remote_user_middleware = 'django.contrib.auth.middleware.RemoteUserMiddleware'
        if not remote_user_middleware in settings.MIDDLEWARE_CLASSES:
            settings.MIDDLEWARE_CLASSES += (remote_user_middleware,)

        auth_backends = list(settings.AUTHENTICATION_BACKENDS)
        try:
            index = auth_backends.index('django.contrib.auth.backends.ModelBackend')
            auth_backends[index] = 'django.contrib.auth.backends.RemoteUserBackend'
        except ValueError:
            auth_backends.append('django.contrib.auth.backends.RemoteUserBackend')
        settings.AUTHENTICATION_BACKENDS = auth_backends

    def _unpatch_settings(self):
        ''' Restore settings to before-patching state '''
        settings.MIDDLEWARE_CLASSES = self._MIDDLEWARE_CLASSES
        settings.AUTHENTICATION_BACKENDS = self._AUTHENTICATION_BACKENDS

    def __call__(self, result=None):
        self._patch_settings()
        self.app = DjangoTestApp(extra_environ=self.extra_environ)
        res = super(WebTest, self).__call__(result)
        self._unpatch_settings()
        return res
