#!/usr/bin/python3

from urllib.parse import unquote
from tornado import web,gen
from tornado.concurrent import run_on_executor
from concurrent.futures import ThreadPoolExecutor
from db_query import DBQuery
import os
import json

class SearchHandler(web.RequestHandler):
    def __init__(self, app, request, **kwargs):
        super(SearchHandler, self).__init__(app, request, **kwargs)
        self.executor= ThreadPoolExecutor(8)
        self.dbhost=os.environ["DBHOST"]

    def check_origin(self, origin):
        return True

    @run_on_executor
    def _search(self, index, queries, size, office):
        db=DBQuery(index=index,office=office,host=self.dbhost)
        try:
            return list(db.search(queries,size))
        except Exception as e:
            return str(e)

    @gen.coroutine
    def get(self):
        queries=unquote(str(self.get_argument("queries")))
        index=unquote(str(self.get_argument("index")))
        size=int(self.get_argument("size"))
        office=unquote(str(self.get_argument("office")))
        if office!="*": office=office.split(",")

        r=yield self._search(index, queries, size, office)
        if isinstance(r, str):
            self.set_status(400, str(r))
            return

        self.write({"response":r})
        self.set_status(200, 'OK')
        self.finish()
