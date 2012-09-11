# -*- coding: utf-8 -*-
from django.conf import settings
from django.contrib.auth.models import User
from django.test.signals import template_rendered
from django.core.handlers.wsgi import WSGIHandler
from django.test import TestCase
from django.test.client import store_rendered_templates
from django.utils.functional import curry
from django.utils.importlib import import_module
from webtest import TestApp
from webtest.compat import to_string

from django_webtest.middleware import DjangoWsgiFix
from django_webtest.response import DjangoWebtestResponse

try:
    from django.core.servers.basehttp import AdminMediaHandler as StaticFilesHandler
except ImportError:
    from django.contrib.staticfiles.handlers import StaticFilesHandler


class DjangoTestApp(TestApp):

    def __init__(self, extra_environ=None, relative_to=None):
        super(DjangoTestApp, self).__init__(self.get_wsgi_handler(), extra_environ, relative_to)

    def get_wsgi_handler(self):
        return DjangoWsgiFix(StaticFilesHandler(WSGIHandler()))

    def _update_environ(self, environ, user):
        if user:
            environ = environ or {}
            if isinstance(user, User):
                environ['WEBTEST_USER'] = to_string(user.username)
            else:
                environ['WEBTEST_USER'] = to_string(user)
        return environ

    def do_request(self, req, status, expect_errors):
        req.environ.setdefault('REMOTE_ADDR', '127.0.0.1')

        # is this a workaround for https://code.djangoproject.com/ticket/11111 ?
        req.environ['REMOTE_ADDR'] = to_string(req.environ['REMOTE_ADDR'])
        req.environ['PATH_INFO'] = to_string(req.environ['PATH_INFO'])

        # Curry a data dictionary into an instance of the template renderer
        # callback function.
        data = {}
        on_template_render = curry(store_rendered_templates, data)
        template_rendered.connect(on_template_render)

        response = super(DjangoTestApp, self).do_request(req, status, expect_errors)

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

        response.__class__ = DjangoWebtestResponse
        return response

    def get(self, url, params=None, headers=None, extra_environ=None,
            status=None, expect_errors=False, user=None, auto_follow=False,
            content_type=None):
        extra_environ = self._update_environ(extra_environ, user)
        response = super(DjangoTestApp, self).get(
                  url, params, headers, extra_environ, status, expect_errors)

        is_redirect = lambda r: r.status_int >= 300 and r.status_int < 400
        while auto_follow and is_redirect(response):
            response = response.follow()

        return response

    def post(self, url, params='', headers=None, extra_environ=None,
             status=None, upload_files=None, expect_errors=False,
             content_type=None, user=None):
        extra_environ = self._update_environ(extra_environ, user)
        return super(DjangoTestApp, self).post(
                   url, params, headers, extra_environ, status,
                   upload_files, expect_errors, content_type)

    def put(self, url, params='', headers=None, extra_environ=None,
             status=None, upload_files=None, expect_errors=False,
             content_type=None, user=None):
        extra_environ = self._update_environ(extra_environ, user)
        return super(DjangoTestApp, self).put(
                   url, params, headers, extra_environ, status,
                   upload_files, expect_errors, content_type)

    def delete(self, url, params='', headers=None, extra_environ=None,
             status=None, expect_errors=False,
             content_type=None, user=None):
        extra_environ = self._update_environ(extra_environ, user)
        return super(DjangoTestApp, self).delete(
                   url, params, headers, extra_environ, status,
                   expect_errors, content_type)

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

class WebTest(TestCase):

    extra_environ = {}
    csrf_checks = True
    setup_auth = True

    def _patch_settings(self):
        '''
        Patches settings to add support for django-webtest authorization
        and (optional) to disable CSRF checks.
        '''

        self._DEBUG_PROPAGATE_EXCEPTIONS = settings.DEBUG_PROPAGATE_EXCEPTIONS
        self._MIDDLEWARE_CLASSES = settings.MIDDLEWARE_CLASSES[:]
        self._AUTHENTICATION_BACKENDS = settings.AUTHENTICATION_BACKENDS[:]

        settings.MIDDLEWARE_CLASSES = list(settings.MIDDLEWARE_CLASSES)
        settings.AUTHENTICATION_BACKENDS = list(settings.AUTHENTICATION_BACKENDS)
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
        disable_csrf_middleware = 'django_webtest.middleware.DisableCSRFCheckMiddleware'
        if not disable_csrf_middleware in settings.MIDDLEWARE_CLASSES:
            settings.MIDDLEWARE_CLASSES.insert(0, disable_csrf_middleware)

    def _setup_auth_middleware(self):
        webtest_auth_middleware = 'django_webtest.middleware.WebtestUserMiddleware'
        django_auth_middleware = 'django.contrib.auth.middleware.AuthenticationMiddleware'

        if django_auth_middleware not in settings.MIDDLEWARE_CLASSES:
            # There can be a custom AuthenticationMiddleware subclass or replacement,
            # we can't compute its index so just put our auth middleware to the end.
            # If appending causes problems _setup_auth_middleware method can
            # be overriden by a subclass.
            settings.MIDDLEWARE_CLASSES.append(webtest_auth_middleware)
        else:
            index = settings.MIDDLEWARE_CLASSES.index(django_auth_middleware)
            settings.MIDDLEWARE_CLASSES.insert(index+1, webtest_auth_middleware)

    def _setup_auth_backend(self):
        backend_name = 'django_webtest.backends.WebtestUserBackend'
        settings.AUTHENTICATION_BACKENDS.insert(0, backend_name)

    def renew_app(self):
        """
        Resets self.app (drops the stored state): cookies, etc.
        Note: this renews only self.app, not the responses fetched by self.app.
        """
        self.app = DjangoTestApp(extra_environ=self.extra_environ)

    def __call__(self, result=None):
        self._patch_settings()
        self.renew_app()
        res = super(WebTest, self).__call__(result)
        self._unpatch_settings()
        return res
