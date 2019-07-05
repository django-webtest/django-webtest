
CHANGES
=======

1.9.7 (2019-07-05)
------------------

- allow overriding HTTP_HOST with DjangoTestApp.__init__. Fixed #102


1.9.6 (2019-06-07)
------------------

- rest_framework auth class. Fixed #98 #100


1.9.5 (2019-05-31)
------------------

- Fix compatibility with django 3. See #96

- Add integration with django-rest-framework auth

- Add missing args to DjangoTestApp. Fixed #86

1.9.4 (2018-10-27)
------------------

- py34 and Django 1.8 are no longer tested (but may works)

- allow to use positionnal args; fixed #89

- remove deprecated pytest.yield_fixture functions. use pytest.fixture instead;
  fixed #88

- Don't add duplicate WebtestUserMiddleware to the list of middlewares in
  WebTestMixin. fixed #87

- restore MIDDLEWARE_CLASSES support; fixed #84

1.9.3 (2018-05-03)
------------------

- Passing `user=None` to get/post/etc. methods will clear a user
  previously set with `set_user` instead of doing nothing.

- Avoid sharing settings between tests in pytest plugin

- Fix middleware settings name used


1.9.2 (2017-05-17)
------------------

- silence warnings about is_authenticated on 1.11

- include correct hostname (testserver) when using set_cookie


1.9.1 (2017-03-09)
------------------

- Fix package description (multiline are no longer allowed by pypi)


1.9.0 (2017-03-09)
------------------

- Backward incompatibility: positionnal arguments are no longer supported.
  You'll need to replace them by keywords arguments.

- Added support for Django 1.11

- Dropped support for Django <= 1.7

- Dropped support for Python 2.6

- Changed value of `HTTP_HOST` header from `localhost` to `testserver`, to
  match behaviour of Django test client.

- Fixed `DjangoTestApp.options`

- Added `DjangoTestApp.head`

- Added pytest fixtures


1.8.0 (2016-09-14)
------------------

- Fixed issue #40 - combining ``app.get`` ``auto_follow=True`` with other
  keyword args.

- Add compatibility to the MIDDLEWARE setting introduced in django 1.10

- Drop support for django 1.2

1.7.9 (2016-04-19)
------------------

- Add set_user() to allow to set a user globally for the app

- Allow 'click' to be given a user param

- Mention testapp.reset() in readme

- Allow to use ``json_`` methods

1.7.8 (2015-04-21)
------------------

- setup.py is switched to setuptools; WebTest is now installed automatically
  (thanks Eric Araujo);
- importlib from stdlib is used when available, for django 1.9 compatibility
  (thanks Helen Sherwood-Taylor);
- django-webtest's own tests are fixed to work in django 1.6+;
- https://bitbucket.org/kmike/django-webtest repository is no longer supported.

1.7.7 (2014-03-25)
------------------

- Fix installation for Python 3.x on systems with C locales.

1.7.6 (2014-01-20)
------------------

- DjangoTestApp methods pass all custom keyword arguments to webtest.TestApp;
  this allows to use ``xhr=True`` feature (thanks Max Kharandziuk).
- Travis CI testing fixes (thanks Darian Moody).

1.7.5 (2013-07-17)
------------------

- OPTIONS method is fixed;
- added workaround for DELETE method warnings
  (see https://github.com/Pylons/webtest/issues/50).

1.7.4 (2013-07-14)
------------------

- Really add ``TransactionWebTest`` base class (thanks Julien Aubert).

1.7.3 (2013-07-07)
------------------

- Added support for PATCH and OPTIONS HTTP methods (thanks Will Bradley).

1.7.2 (2013-06-27)
------------------

- ``TransactionWebTest`` base class is added (thanks Iurii Kriachko).

1.7.1 (2013-06-11)
------------------

- Added support for non-ascii usernames.

1.7 (2013-05-23)
----------------

- Added support for django 1.6 (thanks Carl Meyer).

1.6.1 (2013-03-31)
------------------

- Added support for django 1.5+ custom user models (thanks Gautier Hayoun).

1.6 (2013-03-07)
----------------

- Added ability to pass a custom response_class and app_class to WebTest
  (thanks Bruno Renié);
- Added case-insensitive header access in DjangoWebtestResponse (thanks
  Bruno Renié).

1.5.7 (2013-02-27)
------------------

- WebTest 2.0 support.

1.5.6 (2013-01-21)
------------------

- django 1.5 support: transaction handling is fixed (thanks Marco Braak).

1.5.5 (2013-01-14)
------------------

- Fixed django 1.5 support: DjangoWebtestResponse.streaming attribute
  is added (thanks David Winterbottom).

1.5.4 (2012-09-13)
------------------

- fix django 1.5 issues with AdminMediaHandler (thanks Tai Lee);
- tox.ini is updated to use latest django versions and the
  official trunk with python3 support;
- django 1.5 SimpleCookie issues are fixed.

1.5.3 (2012-04-25)
------------------

- self.assertRedirects is fixed for authenticated requests.

1.5.2 (2012-04-01)
------------------

- if AuthenticationMiddleware is not in a middleware list,
  WebtestUserMiddleware is put to the end of middlewares in order to
  provide better backward compatibility with 1.4.x in case of custom
  auth middlewares.

1.5.1 (2012-03-22)
------------------

- Fixed handling of forms with method="get". Thanks Jeroen Vloothuis.

1.5 (2012-02-24)
----------------

- WebtestUserMiddleware is inserted after AuthenticationMiddleware, not to
  the end of middleware list (thanks bigkevmcd);
- don't list python 2.5 as supported because WebOb dropped 2.5 support;
- python 3 support;
- test running using tox.

1.4.4 (2012-02-08)
------------------

- 'user' parameter for ``self.app.put`` and ``self.app.delete`` methods (thanks
  Ruslan Popov).

1.4.3 (2011-09-27)
------------------

- The django session dictionary is available via ``self.app.session``.

1.4.2 (2011-08-26)
------------------

- ``REMOTE_ADDR`` is now ``'127.0.0.1'`` by default. This is how
  standard django's test client behave.

  Please note that this can slow tests down and cause other side effects
  if django-debug-toolbar 0.9.x is installed+configured and
  ``INTERNAL_IPS`` contain ``'127.0.0.1'`` because debug toolbar will
  become turned on during tests. The workaround is to remove
  django-debug-toolbar middleware during tests in your test settings::

      DEBUG_MIDDLEWARE = 'debug_toolbar.middleware.DebugToolbarMiddleware'
      if DEBUG_MIDDLEWARE in MIDDLEWARE_CLASSES:
          MIDDLEWARE_CLASSES.remove(DEBUG_MIDDLEWARE)


1.4.1 (2011-06-29)
------------------

- ``self.renew_app()`` method for resetting the 'browser' inside tests.

1.4 (2011-06-23)
----------------

- Better auth implementation;
- support for assertRedirects, assertContains and assertNotContains.

1.3 (2010-12-31)
----------------

- Django 1.3 compatibility: test responses are now having 'templates' attribute;
- Django 1.3 compatibility: the way exceptions are handled is changed;
- auto_follow parameter for app.get method (redirect chains will be
  auto-followed with auto_follow=True).

1.2.1 (2010-08-24)
------------------

- REMOTE_USER authorization can be disabled.

1.2 (2010-08-21)
----------------

- ``response.template`` and ``response.context`` goodness (thanks Gregor Müllegger);
- tests (thanks Gregor Müllegger);
- csrf checks are now optional (thanks Gregor Müllegger).

1.1.1 (2010-07-16)
------------------

- User instance can be passed to `get` and `post` methods instead
  of user's username.

1.1 (2010-06-15)
----------------

- Original traceback instead of html 500 error page;
- per-TestCase extra_environ (thanks Gael Pasgrimaud);
- fixed a bug with app.post parameters (thanks anonymous).


1.0 (2010-04-20)
----------------
Initial release (thanks Ian Bicking for WebTest).
