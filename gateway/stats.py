#!/usr/bin/python3

from urllib.parse import unquote
from tornado import web,gen
from tornado.concurrent import run_on_executor
from concurrent.futures import ThreadPoolExecutor
from db_query import DBQuery
from language import encode
from configuration import env
import json

dbhost=env["DBHOST"]
office=list(map(float,env["OFFICE"].split(","))) if "OFFICE" in env else ""

class StatsHandler(web.RequestHandler):
    def __init__(self, app, request, **kwargs):
        super(StatsHandler, self).__init__(app, request, **kwargs)
        self.executor= ThreadPoolExecutor(4)

    def check_origin(self, origin):
        return True

    @run_on_executor
    def _stats(self, index, queries, fields):
        try:
            dbq=DBQuery(index=index,office=office,host=dbhost)
            return dbq.stats(queries, fields)
        except Exception as e:
            return str(e)

    @gen.coroutine
    def get(self):
        queries=unquote(str(self.get_argument("queries")))
        index=unquote(str(self.get_argument("index")))
        fields=unquote(str(self.get_argument("fields"))).split(",")

        r=yield self._stats(index, queries, fields)
        if isinstance(r,str):
            self.set_status(400, encode(r))
            return

        self.write(r)
        self.set_status(200,'OK')
        self.finish()
