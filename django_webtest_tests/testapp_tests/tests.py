# -*- coding: utf-8 -*-
from django.core import mail
from django.test import TestCase


class GetPostRequestTest(TestCase):
    def test_fail(self):
        self.fail(1)
