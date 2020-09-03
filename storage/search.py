#!/usr/bin/python3

from urllib.parse import unquote
from tornado import web,gen
from tornado.concurrent import run_on_executor
from concurrent.futures import ThreadPoolExecutor
from db_query import DBQuery
from language import encode
import os
import json

dbhost=os.environ["DBHOST"]
office=list(map(float,os.environ["OFFICE"].split(","))) if "OFFICE" in os.environ else ""

class SearchHandler(web.RequestHandler):
    def __init__(self, app, request, **kwargs):
        super(SearchHandler, self).__init__(app, request, **kwargs)
        self.executor= ThreadPoolExecutor(4)

    def check_origin(self, origin):
        return True

    @run_on_executor
    def _search(self, index, queries, size):
        try:
            dbq=DBQuery(index=index,office=office,host=dbhost)
            return list(dbq.search(queries,size))
        except Exception as e:
            return str(e)

    @gen.coroutine
    def get(self):
        queries=unquote(str(self.get_argument("queries")))
        index=unquote(str(self.get_argument("index")))
        size=int(self.get_argument("size"))

        r=yield self._search(index, queries, size)
        if isinstance(r, str):
            self.set_status(400, encode(r))
            return

        self.write({"response":r})
        self.set_status(200, 'OK')
        self.finish()
