# -*- coding: utf-8 -*-


class DisableCSRFCheckMiddleware(object):
    def process_request(self, request):
        request._dont_enforce_csrf_checks = True
