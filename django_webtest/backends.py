from django.contrib.auth.backends import RemoteUserBackend

class WebtestUserBackend(RemoteUserBackend):
    """ Auth backend for django-webtest auth system """

    def authenticate(self, django_webtest_user):
        return super(WebtestUserBackend, self).authenticate(django_webtest_user)

