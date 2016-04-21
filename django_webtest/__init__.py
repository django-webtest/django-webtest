# -*- coding: utf-8 -*-
from django.conf import settings
from django.test.signals import template_rendered
from django.core.handlers.wsgi import WSGIHandler
from django.test import TestCase, TransactionTestCase
from django.test.client import store_rendered_templates
from django.utils.functional import curry

try:
    from importlib import import_module
except ImportError:
    from django.utils.importlib import import_module

from django.core import signals
try:
    from django.db import close_old_connections
except ImportError:
    from django.db import close_connection
    close_old_connections = None
try:
    from django.core.servers.basehttp import (
        AdminMediaHandler as StaticFilesHandler)
except ImportError:
    from django.contrib.staticfiles.handlers import StaticFilesHandler

from webtest import TestApp
try:
    from webtest.utils import NoDefault
except ImportError:
    NoDefault = ''

from django_webtest.response import DjangoWebtestResponse
from django_webtest.compat import to_string, to_wsgi_safe_string


class DjangoTestApp(TestApp):
    response_class = DjangoWebtestResponse

    def __init__(self, extra_environ=None, relative_to=None):
        super(DjangoTestApp, self).__init__(self.get_wsgi_handler(),
                                            extra_environ, relative_to)

    def get_wsgi_handler(self):
        return StaticFilesHandler(WSGIHandler())

    def set_user(self, user=None):
        """Update the user used by the app globaly. If user is None then user
        is unset"""
        if user is None and 'WEBTEST_USER' in self.extra_environ:
            del self.extra_environ['WEBTEST_USER']
        if user is not None:
            self.extra_environ = self._update_environ(self.extra_environ, user)

    def _update_environ(self, environ, user):
        if user:
            environ = environ or {}
            username = _get_username(user)
            environ['WEBTEST_USER'] = to_wsgi_safe_string(username)
        return environ

    def _update_kwargs(self, kwargs):
        if 'user' in kwargs:
            user = kwargs.pop('user', None)
            extra_environ = kwargs.get('extra_environ', {})
            kwargs['extra_environ'] = self._update_environ(extra_environ, user)
        return kwargs

    def do_request(self, req, status, expect_errors):

        # Django closes the database connection after every request;
        # this breaks the use of transactions in your tests.
        if close_old_connections is not None:  # Django 1.6+
            signals.request_started.disconnect(close_old_connections)
            signals.request_finished.disconnect(close_old_connections)
        else:  # Django < 1.6
            signals.request_finished.disconnect(close_connection)

        try:
            req.environ.setdefault('REMOTE_ADDR', '127.0.0.1')

            # is this a workaround for
            # https://code.djangoproject.com/ticket/11111 ?
            req.environ['REMOTE_ADDR'] = to_string(req.environ['REMOTE_ADDR'])
            req.environ['PATH_INFO'] = to_string(req.environ['PATH_INFO'])

            # Curry a data dictionary into an instance of the template renderer
            # callback function.
            data = {}
            on_template_render = curry(store_rendered_templates, data)
            template_rendered.connect(on_template_render)

            response = super(DjangoTestApp, self).do_request(req, status,
                                                             expect_errors)

            # Add any rendered template detail to the response.
            # If there was only one template rendered (the most likely case),
            # flatten the list to a single element.
            def flattend(detail):
                if len(data[detail]) == 1:
                    return data[detail][0]
                return data[detail]

            response.context = None
            response.template = None
            response.templates = data.get('templates', None)

            if data.get('context'):
                response.context = flattend('context')

            if data.get('template'):
                response.template = flattend('template')
            elif data.get('templates'):
                response.template = flattend('templates')

            response.__class__ = self.response_class
            return response
        finally:
            if close_old_connections:  # Django 1.6+
                signals.request_started.connect(close_old_connections)
                signals.request_finished.connect(close_old_connections)
            else:  # Django < 1.6
                signals.request_finished.connect(close_connection)

    def get(self, *args, **kwargs):
        auto_follow = kwargs.pop('auto_follow', False)
        self._update_kwargs(kwargs)
        response = super(DjangoTestApp, self).get(*args, **kwargs)

        def is_redirect(r):
            return r.status_int >= 300 and r.status_int < 400
        while auto_follow and is_redirect(response):
            response = response.follow()

        return response

    def post(self, *args, **kwargs):
        self._update_kwargs(kwargs)
        return super(DjangoTestApp, self).post(*args, **kwargs)

    def put(self, *args, **kwargs):
        self._update_kwargs(kwargs)
        return super(DjangoTestApp, self).put(*args, **kwargs)

    def patch(self, *args, **kwargs):
        self._update_kwargs(kwargs)
        return super(DjangoTestApp, self).patch(*args, **kwargs)

    def options(self, *args, **kwargs):
        self._update_kwargs(kwargs)
        return super(DjangoTestApp, self).options(*args, **kwargs)

    def delete(self, *args, **kwargs):
        self._update_kwargs(kwargs)
        return super(DjangoTestApp, self).delete(*args, **kwargs)

    def post_json(self, *args, **kwargs):
        self._update_kwargs(kwargs)
        return super(DjangoTestApp, self).post_json(*args, **kwargs)

    def put_json(self, *args, **kwargs):
        self._update_kwargs(kwargs)
        return super(DjangoTestApp, self).put_json(*args, **kwargs)

    def patch_json(self, *args, **kwargs):
        self._update_kwargs(kwargs)
        return super(DjangoTestApp, self).patch_json(*args, **kwargs)

    def delete_json(self, *args, **kwargs):
        self._update_kwargs(kwargs)
        return super(DjangoTestApp, self).delete_json(*args, **kwargs)

    @property
    def session(self):
        """
        Obtains the current session variables.
        """
        if 'django.contrib.sessions' in settings.INSTALLED_APPS:
            engine = import_module(settings.SESSION_ENGINE)
            cookie = self.cookies.get(settings.SESSION_COOKIE_NAME, None)
            if cookie:
                return engine.SessionStore(cookie)
        return {}


class WebTestMixin(object):

    extra_environ = {}
    csrf_checks = True
    setup_auth = True
    app_class = DjangoTestApp

    def _patch_settings(self):
        '''
        Patches settings to add support for django-webtest authorization
        and (optional) to disable CSRF checks.
        '''

        self._DEBUG_PROPAGATE_EXCEPTIONS = settings.DEBUG_PROPAGATE_EXCEPTIONS
        self._MIDDLEWARE_CLASSES = settings.MIDDLEWARE_CLASSES[:]
        self._AUTHENTICATION_BACKENDS = settings.AUTHENTICATION_BACKENDS[:]

        settings.MIDDLEWARE_CLASSES = list(settings.MIDDLEWARE_CLASSES)
        settings.AUTHENTICATION_BACKENDS = list(
            settings.AUTHENTICATION_BACKENDS)
        settings.DEBUG_PROPAGATE_EXCEPTIONS = True

        if not self.csrf_checks:
            self._disable_csrf_checks()

        if self.setup_auth:
            self._setup_auth()

    def _unpatch_settings(self):
        ''' Restores settings to before-patching state '''
        settings.MIDDLEWARE_CLASSES = self._MIDDLEWARE_CLASSES
        settings.AUTHENTICATION_BACKENDS = self._AUTHENTICATION_BACKENDS
        settings.DEBUG_PROPAGATE_EXCEPTIONS = self._DEBUG_PROPAGATE_EXCEPTIONS

    def _setup_auth(self):
        ''' Setups django-webtest authorization '''
        self._setup_auth_middleware()
        self._setup_auth_backend()

    def _disable_csrf_checks(self):
        disable_csrf_middleware = (
            'django_webtest.middleware.DisableCSRFCheckMiddleware')
        if disable_csrf_middleware not in settings.MIDDLEWARE_CLASSES:
            settings.MIDDLEWARE_CLASSES.insert(0, disable_csrf_middleware)

    def _setup_auth_middleware(self):
        webtest_auth_middleware = (
            'django_webtest.middleware.WebtestUserMiddleware')
        django_auth_middleware = (
            'django.contrib.auth.middleware.AuthenticationMiddleware')

        if django_auth_middleware not in settings.MIDDLEWARE_CLASSES:
            # There can be a custom AuthenticationMiddleware subclass or
            # replacement, we can't compute its index so just put our auth
            # middleware to the end.  If appending causes problems
            # _setup_auth_middleware method can be overriden by a subclass.
            settings.MIDDLEWARE_CLASSES.append(webtest_auth_middleware)
        else:
            index = settings.MIDDLEWARE_CLASSES.index(django_auth_middleware)
            settings.MIDDLEWARE_CLASSES.insert(index + 1,
                                               webtest_auth_middleware)

    def _setup_auth_backend(self):
        backend_name = 'django_webtest.backends.WebtestUserBackend'
        settings.AUTHENTICATION_BACKENDS.insert(0, backend_name)

    def renew_app(self):
        """
        Resets self.app (drops the stored state): cookies, etc.
        Note: this renews only self.app, not the responses fetched by self.app.
        """
        self.app = self.app_class(extra_environ=self.extra_environ)

    def __call__(self, result=None):
        self._patch_settings()
        self.renew_app()
        res = super(WebTestMixin, self).__call__(result)
        self._unpatch_settings()
        return res


class WebTest(WebTestMixin, TestCase):
    pass


class TransactionWebTest(WebTestMixin, TransactionTestCase):
    pass


def _get_username(user):
    """
    Return user's username. ``user`` can be standard Django User
    instance, a custom user model or just an username (as string).
    """
    if hasattr(user, 'get_username'):  # custom user, django 1.5+
        return user.get_username()
    elif hasattr(user, 'username'):    # standard User
        return user.username
    else:                              # assume user is just an username
        return user
