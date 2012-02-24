# -*- coding: utf-8 -*-
from __future__ import absolute_import

class UserMiddleware(object):
    def process_request(self, request):
        request.user.processed = True