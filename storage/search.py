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
            return {"response":list(dbq.search(queries,size))}
        except Exception as e:
            return {"response":[], "status":str(e)}

    @gen.coroutine
    def get(self):
        queries=unquote(str(self.get_argument("queries")))
        index=unquote(str(self.get_argument("index")))
        size=int(self.get_argument("size"))

        r=yield self._search(index, queries, size)
        self.write(r)
