# -*- coding: utf-8 -*-
from django_webtest import WebTestMixin
import pytest


@pytest.fixture(scope='session')
def django_app_mixin():
    app_mixin = WebTestMixin()
    return app_mixin


@pytest.yield_fixture
def django_app(django_app_mixin):
    django_app_mixin._patch_settings()
    django_app_mixin.renew_app()
    yield django_app_mixin.app
    django_app_mixin._unpatch_settings()


@pytest.yield_fixture
def django_app_factory():
    app_mixin = WebTestMixin()

    def factory(csrf_checks=True, extra_environ=None):
        app_mixin.csrf_checks = csrf_checks
        if extra_environ:
            app_mixin.extra_environ = extra_environ
        app_mixin._patch_settings()
        app_mixin.renew_app()
        return app_mixin.app

    yield factory
    app_mixin._unpatch_settings()
