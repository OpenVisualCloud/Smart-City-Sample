#!/usr/bin/python3

from urllib.parse import unquote
from tornado import web,gen
from tornado.concurrent import run_on_executor
from concurrent.futures import ThreadPoolExecutor
from db_query import DBQuery

class CountHandler(web.RequestHandler):
    def __init__(self, app, request, **kwargs):
        super(CountHandler, self).__init__(app, request, **kwargs)
        self.executor= ThreadPoolExecutor(8)

    def check_origin(self, origin):
        return True

    @run_on_executor
    def _count(self, index, queries):
        db=DBQuery(index)
        try:
            return db.count(queries)
        except Exception as e:
            return str(e)

    @gen.coroutine
    def get(self):
        queries=unquote(str(self.get_argument("queries")))
        index=unquote(str(self.get_argument("index")))

        r=yield self._count(index, queries)
        if isinstance(r,str):
            self.set_status(400, str(r))
            return

        self.write(str(r))
        self.set_header('Content-Type','text/plain')
        self.set_status(200,'OK')
        self.finish()
