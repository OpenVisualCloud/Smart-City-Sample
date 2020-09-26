#!/usr/bin/python3

from tornado import web, gen

class AuthHandler(web.RequestHandler):
    def __init__(self, app, request, **kwargs):
        super(AuthHandler, self).__init__(app, request, **kwargs)

    def check_origin(self, origin):
        return True

    @gen.coroutine
    def get(self):
        self.set_status(200,'OK')

