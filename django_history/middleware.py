# -*- coding:utf-8 -*-
from threading import local


thread_namespace = local()


class CurrenUserMiddleware:
    def process_request(self, request):
        thread_namespace.user = getattr(request, 'user', None)

    def process_response(self, request, response):
        thread_namespace.user = None
        return response
