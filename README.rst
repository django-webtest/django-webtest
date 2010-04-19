==============
django-webtest
==============

django-webtest is an almost trivial app for instant integration of
Ian Bicking's WebTest (http://pythonpaste.org/webtest/) with django's
testing framework.


Installation
============

::
    $ pip install webtest
    $ pip install django-webtest

or ::

    $ easy_install webtest
    $ easy_install django-webtest

or grab latest versions from bitbucket
(http://bitbucket.org/ianb/webtest, http://bitbucket.org/kmike/django-webtest)

Usage
=====

django-webtest provides django.test.TestCase subclass (``WebTest``) that creates
``webtest.TestApp`` around django wsgi interface and make it available in
tests as ``self.app``.

It also features optional ``user`` argument for ``self.app.get`` and
``self.app.post`` methods to help making authorized requests. This argument
should be django.contrib.auth.models.User's ``username`` for user who is
supposed to be logged in.

All of these features can be easily set up manually (thanks to WebTest
architecture) and they are even not neccessary for using WebTest with django but
it is nice to have some sort of integration instantly.

::

    from django_webtest import WebTest

    class MyTestCase(WebTest):

        # we want some initial data to be able to login
        fixtures = ['users', 'blog_posts']

        def testBlog(self):
            # pretend to be logged in as user `kmike` and go to the index page
            index = self.app.get('/', user='kmike')

            # All the webtest API is available. For example, we click
            # on a <a href='/tech-blog/'>Blog</a> link, check that it
            # works (result page doesn't raise exceptions and returns 200 http
            # code) and test if result page have 'My Article' text in
            # it's body.
            assert 'My Article' in index.click('Blog')

See http://pythonpaste.org/webtest/ for API help. It can follow links, submit
forms, parse html, xml and json responses with different parsing libraries,
upload files and more.

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
non-latin text (not to mention unicode) and have a much larger codebase to
hack on. Twill however understands HTML better and is more mature so
consider it (and django-test-utils package) if WebTest doesn't fit for some
reason.