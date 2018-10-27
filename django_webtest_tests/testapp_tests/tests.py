# -*- coding: utf-8 -*-
from __future__ import unicode_literals, absolute_import


import django
from django.contrib.auth.models import User
try:
    from django.urls import reverse
except ImportError:
    from django.core.urlresolvers import reverse
from django.test.testcases import override_settings
from unittest import skipIf


from webtest import AppError, TestApp

from django_webtest import WebTest
from django_webtest.compat import is_authenticated, is_anonymous


class MethodsTest(WebTest):

    csrf_checks = False

    def assertMethodWorks(self, meth, name):
        response = meth('/')
        self.assertEqual(response.status_int, 200)
        response.mustcontain(name)
        #self.assertTrue(name in response)

    def assertMethodWorksXHR(self, meth, name):
        try:
            response = meth('/', xhr=True)
        except TypeError as e:
            # for webtest < 2
            self.assertIn('xhr', e.message)
        else:
            # for webtest == 2
            self.assertEqual(response.status_int, 200)
            response.mustcontain(name)

    def test_get(self):
        self.assertMethodWorks(self.app.get, 'GET')

    def test_post(self):
        self.assertMethodWorks(self.app.post, 'POST')

    def test_put(self):
        self.assertMethodWorks(self.app.put, 'PUT')

    def test_delete(self):
        self.assertMethodWorks(self.app.delete, 'DELETE')

    def test_get_json(self):
        self.assertMethodWorks(self.app.get, 'GET')

    def test_post_json(self):
        self.assertMethodWorks(self.app.post_json, 'POST')

    def test_put_json(self):
        self.assertMethodWorks(self.app.put_json, 'PUT')

    def test_delete_json(self):
        self.assertMethodWorks(self.app.delete_json, 'DELETE')

    def test_get_xhr(self):
        self.assertMethodWorksXHR(self.app.get, 'GET')

    def test_post_xhr(self):
        self.assertMethodWorksXHR(self.app.post, 'POST')

    def test_put_xhr(self):
        self.assertMethodWorksXHR(self.app.put, 'PUT')

    def test_delete_xhr(self):
        self.assertMethodWorksXHR(self.app.delete, 'DELETE')

    if hasattr(TestApp, 'patch'):  # old WebTest versions don't have 'patch' method
        def test_patch(self):
            self.assertMethodWorks(self.app.patch, 'PATCH')

    def test_head(self):
        response = self.app.head('/')
        self.assertEqual(response.status_int, 200)
        expected = b'' if django.VERSION < (1, 10) else b'HEAD'
        self.assertEqual(response.body, expected)

    def test_options(self):
        self.assertMethodWorks(self.app.options, 'OPTIONS')

    def test_get_auto_follow_default(self):
        response = self.app.get(reverse('remove-prefix-redirect',
                                        args=('template/index.html',)))
        self.assertEqual(response.status_code, 302)

    def test_get_auto_follow_true(self):
        response = self.app.get(reverse('remove-prefix-redirect',
                                        args=('template/index.html',)),
                                auto_follow=True)
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Hello')

    def test_get_auto_follow_and_expect_errors(self):
        response = self.app.get(reverse('remove-prefix-redirect',
                                        args=('some-404/',)),
                                auto_follow=True, expect_errors=True)
        self.assertEqual(response.status_code, 404)

    def test_get_with_positional_args(self):
        response = self.app.get('/', {})
        self.assertEqual(response.status_code, 200)


class PostRequestTest(WebTest):
    csrf_checks = False

    def test_post_request(self):
        response = self.app.post('/')
        self.assertEqual(response.status_int, 200)
        self.assertTrue('POST' in response)

    def test_404_response(self):
        self.assertRaises(AppError, self.app.get, '/404/')


class CsrfProtectionTest(WebTest):
    def test_csrf_failed(self):
        response = self.app.post('/', expect_errors=True)
        self.assertEqual(response.status_int, 403)


class FormSubmitTest(WebTest):

    def test_form_submit(self):
        page = self.app.get(reverse('check_password'))
        page.form['password'] = 'bar'
        page_with_errors = page.form.submit()

        assert 'Incorrect password' in page_with_errors

        page_with_errors.form['password'] = 'foo'
        page_with_errors.form.submit().follow() # check for 302 response


class GetFormSubmitTest(WebTest):

    def test_form_submit(self):
        page = self.app.get(reverse('search'))
        page.form['q'] = 'bar'
        response = page.form.submit()
        self.assertEqual(response.context['q'], 'bar')


class TemplateContextTest(WebTest):
    def test_rendered_templates(self):
        response = self.app.get('/template/index.html')
        self.assertTrue(hasattr(response, 'context'))
        self.assertTrue(hasattr(response, 'template'))

        self.assertEqual(response.template.name, 'index.html')
        self.assertEqual(response.context['bar'], True)
        self.assertEqual(response.context['spam'], None)
        self.assertRaises(KeyError, response.context.__getitem__, 'invalid')

    def test_multiple_templates(self):
        response = self.app.get('/template/complex.html')
        self.assertEqual(len(response.template), 4)
        self.assertEqual(response.template[0].name, 'complex.html')
        self.assertEqual(response.template[1].name, 'include.html')
        self.assertEqual(response.template[2].name, 'include.html')
        self.assertEqual(response.template[3].name, 'include.html')

        self.assertEqual(response.context['foo'], ('a', 'b', 'c'))
        self.assertEqual(response.context['bar'], True)
        self.assertEqual(response.context['spam'], None)


class BaseAuthTest(WebTest):

    def setUp(self):
        self.user = User.objects.create_user('foo', 'example@example.com', '123')

    def _login(self, username, password):
        form = self.app.get(reverse('auth_login')).form
        form['username'] = username
        form['password'] = password
        return form.submit()

    def assertCanLogin(self, user):
        response = self.app.get('/template/index.html', user=user)
        res_user = response.context['user']
        assert is_authenticated(res_user)

        if isinstance(user, User):
            self.assertEqual(res_user, user)
        else:
            self.assertEqual(res_user.username, user)


class AuthTest(BaseAuthTest):

    def test_not_logged_in(self):
        response = self.app.get('/template/index.html')
        user = response.context['user']
        assert not is_authenticated(user)

    def test_logged_using_username(self):
        self.assertCanLogin('foo')

    def test_logged_using_native_username(self):
        self.assertCanLogin(str('foo'))

    def test_logged_using_unicode_username(self):
        self.assertCanLogin('ƒøø')

    def test_logged_using_instance(self):
        self.assertCanLogin(self.user)

    def test_logged_using_unicode_instance(self):
        user = User.objects.create_user('ƒøø', 'example@example.com', '123')
        self.assertCanLogin(user)

    def test_auth_is_enabled(self):
        from django.conf import settings

        auth_middleware = 'django_webtest.middleware.WebtestUserMiddleware'
        assert auth_middleware in self.settings_middleware
        assert 'django_webtest.backends.WebtestUserBackend' in settings.AUTHENTICATION_BACKENDS

        dependency_index = self.settings_middleware.index(
            'django.contrib.auth.middleware.AuthenticationMiddleware')

        self.assertEqual(
            self.settings_middleware.index(auth_middleware),
            dependency_index + 1,
        )

    def test_custom_middleware(self):
        response = self.app.get('/template/index.html', user=self.user)
        user = response.context['user']
        self.assertTrue(user.processed)

    def test_standard_auth(self):
        resp = self._login(self.user.username, '123').follow()
        user = resp.context['user']
        self.assertEqual(user, self.user)

        self.assertIn('sessionid', self.app.cookies)

        resp = self.app.get(reverse('protected'))
        self.assertEquals(resp.status_int, 200)
        resp.mustcontain('ok: {0}'.format(self.user.username))

    def test_reusing_custom_user(self):
        if django.VERSION >= (1, 5):
            from django_webtest_tests.testapp_tests.models import MyCustomUser
            with self.settings(AUTH_USER_MODEL = 'testapp_tests.MyCustomUser'):
                custom_user = MyCustomUser.objects.create(
                        email="custom@example.com")
                custom_user.set_password("123")
                custom_user.save()

                # Let the middleware logs the user in
                self.app.get('/template/index.html', user=custom_user)

                # Middleware authentication check shouldn't crash
                response = self.app.get('/template/index.html',
                        user=custom_user)
                user = response.context['user']
                assert is_authenticated(user)
                self.assertEqual(user, custom_user)

    def test_normal_user(self):
        """Make sure the fix for custom users in django 1.5 doesn't break
        normal django users"""
        self.app.get('/template/index.html', user=self.user)
        self.app.get('/template/index.html', user=self.user)


class GlobalAuthTest(BaseAuthTest):

    def test_set_user(self):
        self.app.set_user(self.user.username)
        environ = self.app.extra_environ
        self.assertEqual(environ['WEBTEST_USER'], self.user.username)

        resp = self.app.get('/template/index.html')

        environ = resp.request.environ
        self.assertEqual(environ['WEBTEST_USER'], self.user.username)
        resp.mustcontain('User: {}'.format(self.user.username))

    def test_set_user_reset(self):
        self.app.set_user(self.user.username)
        self.app.set_user(None)
        environ = self.app.extra_environ
        self.assertNotIn('WEBTEST_USER', environ)

        resp = self.app.get('/template/index.html')

        environ = resp.request.environ
        self.assertNotIn('WEBTEST_USER', environ)
        resp.mustcontain('User: AnonymousUser')

    def test_user_param(self):
        resp = self.app.get('/template/index.html', user='bob_morane')

        self.assertEqual(resp.request.environ['WEBTEST_USER'], 'bob_morane')

        resp.mustcontain('User: bob_morane')

    def test_user_param_reset(self):
        self.app.set_user(self.user.username)
        resp = self.app.get('/template/index.html', user=None)

        # this request had no user
        self.assertEqual(resp.request.environ['WEBTEST_USER'], '')
        resp.mustcontain('User: AnonymousUser')
        # app object is unchanged
        self.assertEqual(self.app.extra_environ['WEBTEST_USER'],
                         self.user.username)


class EnvironTest(BaseAuthTest):

    extra_environ = {'REMOTE_ADDR': '127.0.0.2'}

    def test_extra_environ_reset(self):
        resp = self.app.get('/template/index.html', user=self.user)
        environ = resp.request.environ
        self.assertEqual(environ['WEBTEST_USER'], 'foo')
        self.assertEqual(environ['REMOTE_ADDR'], '127.0.0.2')

        resp2 = self.app.get('/template/index.html')
        environ = resp2.request.environ
        self.assertNotIn('WEBTEST_USER', environ)
        self.assertEqual(environ['REMOTE_ADDR'], '127.0.0.2')

        resp3 = self.app.get('/template/index.html',
                             extra_environ={'REMOTE_ADDR': '127.0.0.1'})
        environ = resp3.request.environ
        self.assertEqual(environ['REMOTE_ADDR'], '127.0.0.1')


class RenewAppTest(BaseAuthTest):

    def test_renew_app(self):
        self._login(self.user.username, '123').follow()

        # auth cookie is preserved between self.app.get calls
        page1 = self.app.get('/template/form.html')
        self.assertEqual(page1.context['user'], self.user)

        self.renew_app()

        # cookies were dropped
        page2 = self.app.get('/template/form.html')
        self.assertTrue(is_anonymous(page2.context['user']))

        # but cookies are still there while browsing from stored page
        page1_1 = page1.click('Login')
        self.assertEqual(page1_1.context['user'], self.user)



class DjangoAssertsTest(BaseAuthTest):

    def test_assert_template_used(self):
        response = self.app.get('/template/index.html')
        self.assertTemplateUsed(response, 'index.html')
        self.assertTemplateNotUsed(response, 'complex.html')

        complex_response = self.app.get('/template/complex.html')
        self.assertTemplateUsed(complex_response, 'complex.html')
        self.assertTemplateUsed(complex_response, 'include.html')
        self.assertTemplateNotUsed(complex_response, 'foo.html')

    def test_assert_form_error(self):
        page = self.app.get(reverse('check_password'))
        page.form['password'] = 'bar'
        page_with_errors = page.form.submit()
        self.assertFormError(page_with_errors, 'form', 'password', 'Incorrect password.')

    def test_assert_contains(self):
        response = self.app.get('/template/index.html')
        self.assertContains(response, 'Hello', 1)
        self.assertNotContains(response, 'Good bye!')

    def test_assert_contains_unicode(self):
        response = self.app.get('/template/index.html')
        self.assertContains(response, 'привет', 2)

    def test_assert_redirects(self):
        page = self.app.get(reverse('check_password'))
        page.form['password'] = 'foo'
        resp = page.form.submit()
        self.assertRedirects(resp, '/')

    def test_redirects_noauth(self):
        self.app.get(reverse('redirect-to-protected')).follow(status=302)

    def test_redirects(self):
        self.app.get(reverse('redirect-to-protected'), user=self.user).follow()

    def test_assert_redirects_auth(self):
        page = self.app.get(reverse('redirect-to-protected'), user=self.user)
        self.assertRedirects(page, reverse('protected'))



class DisableAuthSetupTest(WebTest):
    setup_auth = False

    def test_no_auth(self):
        from django.conf import settings
        middleware = getattr(settings, 'MIDDLEWARE', None) or settings.MIDDLEWARE_CLASSES
        assert 'django_webtest.middleware.WebtestUserMiddleware' not in middleware
        assert 'django_webtest.backends.WebtestUserBackend' not in settings.AUTHENTICATION_BACKENDS


class TestSession(WebTest):

    def test_session_not_set(self):
        response = self.app.get('/')
        self.assertEqual(response.status_int, 200)
        self.assertEqual({}, self.app.session)

    def test_sessions_disabled(self):
        from django.conf import settings

        apps = list(settings.INSTALLED_APPS)
        apps.remove("django.contrib.sessions")
        settings.INSTALLED_APPS= apps

        response = self.app.get('/')
        self.assertEqual(response.status_int, 200)
        self.assertEqual({}, self.app.session)

    def test_session_not_empty(self):
        self.app.get(reverse('set_session'))
        self.assertEqual('foo', self.app.session['test'])


class TestHeaderAccess(WebTest):
    def test_headers(self):
        response = self.app.get('/')
        self.assertEqual(response['Content-Type'], 'text/html; charset=utf-8')
        self.assertEqual(response['content-type'], 'text/html; charset=utf-8')

    def test_bad_header(self):
        def access_bad_header():
            response = self.app.get('/')
            response['X-Unknown-Header']
        self.assertRaises(KeyError, access_bad_header)

class TestCookies(WebTest):
    def test_cookies(self):
        self.app.set_cookie(str('test_cookie'), str('cookie monster!'))
        rsp = self.app.get(reverse('cookie_test'))
        self.assertContains(rsp, 'cookie monster!')


@skipIf(django.VERSION < (1, 10), 'MIDDLEWARE is added in Django 1.10')
@override_settings(MIDDLEWARE=[])
class MiddlewareTest(WebTest):

    def test_middleware_setting_name(self):
        self.assertEqual(
            self.middleware_setting_name,
            'MIDDLEWARE'
        )


@skipIf(django.VERSION < (1, 10) or django.VERSION >= (2, 0),
        'MIDDLEWARE is added in Django 1.10')
@override_settings(MIDDLEWARE=None, MIDDLEWARE_CLASSES=[])
class MiddlewareClassesTest(WebTest):

    def test_middleware_setting_name(self):
        self.assertEqual(
            self.middleware_setting_name,
            'MIDDLEWARE_CLASSES'
        )
