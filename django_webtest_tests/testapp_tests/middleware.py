# -*- coding: utf-8 -*-
from __future__ import absolute_import
import django
if django.VERSION >= (1, 10):
    from django.utils.deprecation import MiddlewareMixin
else:
    MiddlewareMixin = object

class UserMiddleware(MiddlewareMixin):
    def process_request(self, request):
        request.user.processed = True
