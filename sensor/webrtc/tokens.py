#!/usr/bin/python3

from tornado import web, gen
from urllib.parse import unquote
from owtapi import OWTAPI

class TokensHandler(web.RequestHandler):
    def __init__(self, app, request, **kwargs):
        super(TokensHandler, self).__init__(app, request, **kwargs)
        self._owt=OWTAPI()

    def check_origin(self, origin):
        return True

    @gen.coroutine
    def post(self):
        room=str(unquote(self.get_argument("room")))
        user=str(unquote(self.get_argument("user","user")))
        role=str(unquote(self.get_argument("role","presenter")))

        token=self._owt.create_token(room=room,user=user,role=role)
        self.set_header('Content-Type','text/plain')
        self.write(token)
