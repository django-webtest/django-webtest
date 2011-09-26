# -*- coding: utf-8 -*-
from webtest import AppError
from django_webtest import WebTest
from django.contrib.auth.models import User
from django.core.urlresolvers import reverse
from testapp_tests.views import PasswordForm

class GetRequestTest(WebTest):
    def test_get_request(self):
        response = self.app.get('/')
        self.assertEqual(response.status_int, 200)
        self.assertTrue('GET' in response)

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


class AuthTest(BaseAuthTest):

    def test_not_logged_in(self):
        response = self.app.get('/template/index.html')
        user = response.context['user']
        assert not user.is_authenticated()

    def test_logged_using_username(self):
        response = self.app.get('/template/index.html', user='foo')
        user = response.context['user']
        assert user.is_authenticated()
        self.assertEqual(user, self.user)

    def test_logged_using_instance(self):
        response = self.app.get('/template/index.html', user=self.user)
        user = response.context['user']
        assert user.is_authenticated()
        self.assertEqual(user, self.user)

    def test_auth_is_enabled(self):
        from django.conf import settings

        auth_middleware = 'django_webtest.middleware.WebtestUserMiddleware'
        assert auth_middleware in settings.MIDDLEWARE_CLASSES
        assert 'django_webtest.backends.WebtestUserBackend' in settings.AUTHENTICATION_BACKENDS
        self.assertEqual(
            settings.MIDDLEWARE_CLASSES.index(auth_middleware),
            len(settings.MIDDLEWARE_CLASSES)-1
        )

    def test_standard_auth(self):
        resp = self._login(self.user.username, '123').follow()
        user = resp.context['user']
        self.assertEqual(user, self.user)


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
        self.assertTrue(page2.context['user'].is_anonymous())

        # but cookies are still there while browsing from stored page
        page1_1 = page1.click('Login')
        self.assertEqual(page1_1.context['user'], self.user)



class DjangoAssertsTest(WebTest):

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
        self.assertContains(response, u'привет', 2)

    def test_assert_redirects(self):
        page = self.app.get(reverse('check_password'))
        page.form['password'] = 'foo'
        resp = page.form.submit()
        self.assertRedirects(resp, '/')


class DisableAuthSetupTest(WebTest):
    setup_auth = False

    def test_no_auth(self):
        from django.conf import settings
        assert 'django_webtest.middleware.WebtestUserMiddleware' not in settings.MIDDLEWARE_CLASSES
        assert 'django_webtest.backends.WebtestUserBackend' not in settings.AUTHENTICATION_BACKENDS

class TestSession(WebTest):

    def test_session_not_set(self):
        response = self.app.get('/')
        self.assertEqual(response.status_int, 200)
        self.assertEquals({}, self.app.session)

    def test_sessions_disabled(self):
        from django.conf import settings

        apps = list(settings.INSTALLED_APPS)
        apps.remove("django.contrib.sessions")
        settings.INSTALLED_APPS= apps

        response = self.app.get('/')
        self.assertEqual(response.status_int, 200)
        self.assertEquals({}, self.app.session)
    
    def test_session_not_empty(self):
        response = self.app.get(reverse('set_session'))
        self.assertEquals('foo', self.app.session['test'])
