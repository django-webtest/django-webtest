# -*- coding: utf-8 -*-

from django.conf import settings

initial_settings = {
    "DEBUG_PROPAGATE_EXCEPTIONS": settings.DEBUG_PROPAGATE_EXCEPTIONS,
    "AUTHENTICATION_BACKENDS": settings.AUTHENTICATION_BACKENDS,
}

def test_django_app(django_app):
    resp = django_app.get('/')
    assert resp.status_int == 200


def test_django_app_post(django_app_factory):
    app = django_app_factory(csrf_checks=False)
    resp = app.post('/')
    assert resp.status_int == 200

def test_app_factory():
    """Ensure django_app_factory properly resets settings."""
    assert settings.DEBUG_PROPAGATE_EXCEPTIONS is initial_settings["DEBUG_PROPAGATE_EXCEPTIONS"]
    assert settings.AUTHENTICATION_BACKENDS == initial_settings["AUTHENTICATION_BACKENDS"]
