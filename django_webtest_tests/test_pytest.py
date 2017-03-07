# -*- coding: utf-8 -*-


def test_django_app(django_app):
    resp = django_app.get('/')
    assert resp.status_int == 200


def test_django_app_post(django_app_factory):
    app = django_app_factory(csrf_checks=False)
    resp = app.post('/')
    assert resp.status_int == 200
