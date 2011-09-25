==============
django-webtest
==============

django-webtest is an app for instant integration of Ian Bicking's
WebTest (http://webtest.pythonpaste.org/) with django's
testing framework.

Usage
=====

::

    from django_webtest import WebTest

    class MyTestCase(WebTest):

        # optional: we want some initial data to be able to login
        fixtures = ['users', 'blog_posts']

        # optional: default extra_environ for this TestCase
        extra_environ = {'HTTP_ACCEPT_LANGUAGE': 'ru'}

        def testBlog(self):
            # pretend to be logged in as user `kmike` and go to the index page
            index = self.app.get('/', user='kmike')

            # All the webtest API is available. For example, we click
            # on a <a href='/tech-blog/'>Blog</a> link, check that it
            # works (result page doesn't raise exceptions and returns 200 http
            # code) and test if result page have 'My Article' text in
            # it's body.
            assert 'My Article' in index.click('Blog')

django-webtest provides django.test.TestCase subclass (``WebTest``) that creates
``webtest.TestApp`` around django wsgi interface and make it available in
tests as ``self.app``.

It also features optional ``user`` argument for ``self.app.get`` and
``self.app.post`` methods to help making authorized requests. This argument
should be django.contrib.auth.models.User instance or a string with user's
``username`` for user who is supposed to be logged in.

For 500 errors original traceback is shown instead of usual html result
from handler500.

You also get the ``response.templates`` and ``response.context`` goodness that
is usually only available if you use django's native test client. These
attributes contain a list of templates that were used to render the response
and the context used to render these templates. All django's native asserts (
``assertFormError``,  ``assertTemplateUsed``, ``assertTemplateNotUsed``,
``assertContains``, ``assertNotContains``, ``assertRedirects``) are
also supported for WebTest responses.

The session dictionary is available via ``self.app.session``, and has the
content as django's native test client.

Unlike django's native test client CSRF checks are not suppressed
by default so missing CSRF tokens will cause test fails (and that's good).

If forms are submitted via WebTest forms API then all form fields (including
CSRF token) are submitted automagically::

    class AuthTest(WebTest):
        fixtures = ['users.json']

        def test_login(self)
            form = self.app.get(reverse('auth_login')).form
            form['username'] = 'foo'
            form['password'] = 'bar'
            response = form.submit().follow()
            self.assertEqual(response.context['user'].username, 'foo')

However if forms are submitted via raw POST requests using ``app.post`` then
csrf tokens become hard to construct. CSRF checks can be disabled by setting
``csrf_checks`` attribute to False in this case::

    class MyTestCase(WebTest):
        csrf_checks = False
        def test_post(self)
            self.app.post('/')

All of these features can be easily set up manually (thanks to WebTest
architecture) and they are even not neccessary for using WebTest with django but
it is nice to have some sort of integration instantly.

See http://webtest.pythonpaste.org/ for API help. It can follow links, submit
forms, parse html, xml and json responses with different parsing libraries,
upload files and more.


Installation
============

::

    $ pip install webtest
    $ pip install django-webtest

Why?
====

While django.test.client.Client is fine for it's purposes, it is not
well-suited for functional or integration testing. From django's test client
docstring:

    This is not intended as a replacement for Twill/Selenium or
    the like - it is here to allow testing against the
    contexts and templates produced by a view, rather than the
    HTML rendered to the end-user.

WebTest plays on the same field as twill. WebTest has nice API, is fast, small,
talk to django application via WSGI instead of HTTP and is an easy way to
write functional/integration/acceptance tests.

Twill is also a great tool and it also can be easily integrated with django
(see django-test-utils package) and I also enjoy it much. But I prefer WebTest
over twill because twill is old (last release is in 2007), communicate via HTTP
instead of WSGI (though there is workaround for that), lacks support for
unicode and have a much larger codebase to hack on. django-webtest also
is able to provide access to the names of rendered templates and
template context just like native django TestClient. Twill however understands
HTML better and is more mature so consider it if WebTest doesn't fit for
some reason.

