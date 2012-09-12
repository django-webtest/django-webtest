# -*- coding: utf-8 -*-

try:
    import urlparse
except ImportError: #python 3
    from urllib import parse as urlparse

from webtest import TestResponse
from django.test import Client
from django.http import SimpleCookie

class DjangoWebtestResponse(TestResponse):
    """
    WebOb's Response quacking more like django's HttpResponse.

    This is here to make more django's TestCase asserts work,
    not to provide a generally useful proxy.
    """
    @property
    def status_code(self):
        return self.status_int

    @property
    def _charset(self):
        return self.charset

    @property
    def content(self):
        return self.body

    @property
    def client(self):
        client = Client()
        client.cookies = SimpleCookie()
        for k,v in self.test_app.cookies.items():
            client.cookies[k] = v
        return client

    def __getitem__(self, item):
        if item != 'Location':
            raise TypeError('Keys other than "Location" are unsupported')

        # django's test response returns location as http://testserver/,
        # WebTest returns it as http://localhost:80/
        e_scheme, e_netloc, e_path, e_query, e_fragment = urlparse.urlsplit(self.location)
        if e_netloc == 'localhost:80':
            e_netloc = 'testserver'
        return urlparse.urlunsplit([e_scheme, e_netloc, e_path, e_query, e_fragment])
