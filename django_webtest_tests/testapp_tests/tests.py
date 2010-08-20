# -*- coding: utf-8 -*-
from webtest import AppError
from django_webtest import WebTest


class GetPostRequestTest(WebTest):
    def test_get_request(self):
        response = self.app.get('/')
        self.assertEqual(response.status_int, 200)
        self.assertTrue('GET' in response)

    def test_post_request(self):
        response = self.app.post('/')
        self.assertEqual(response.status_int, 200)
        self.assertTrue('POST' in response)

    def test_404_response(self):
        self.assertRaises(AppError, self.app.get, '/404/')
