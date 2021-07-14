#!/usr/bin/python3

from tornado import web, gen
from tornado.concurrent import run_on_executor
from concurrent.futures import ThreadPoolExecutor

class AuthHandler(web.RequestHandler):
    def __init__(self, app, request, **kwargs):
        super(AuthHandler, self).__init__(app, request, **kwargs)
        self.executor=ThreadPoolExecutor(4)

    def check_origin(self, origin):
        return True

    @run_on_executor
    def _auth(self, uri, auth):
        print("URI: {} Auth: {}".format(uri, auth), flush=True)
        return (200,'OK')

    @gen.coroutine
    def get(self):
        r=yield self._auth(
            self.request.headers.get("X-Original-URI"),
            self.request.headers.get("Authroization")
        )
        self.set_status(r[0], r[1])
