#!/usr/bin/python3

from urllib.parse import unquote
from tornado import web,gen
from tornado.concurrent import run_on_executor
from concurrent.futures import ThreadPoolExecutor
from db_query import DBQuery
import os

class StatsHandler(web.RequestHandler):
    def __init__(self, app, request, **kwargs):
        super(StatsHandler, self).__init__(app, request, **kwargs)
        self.executor= ThreadPoolExecutor(8)
        self.dbhost=os.environ["DBHOST"]

    def check_origin(self, origin):
        return True

    @run_on_executor
    def _bucketize(self, index, queries, aggs):
        db=DBQuery(index=index,office="*",host=self.dbhost)
        try:
            buckets=db.bucketize(queries, aggs)
        except Exception as e:
            return str(e)
        # reformat buckets to have str keys
        buckets1={}
        for k in buckets: buckets1[str(k)]=buckets[k]
        return buckets1

    @gen.coroutine
    def get(self):
        queries=unquote(str(self.get_argument("queries")))
        index=unquote(str(self.get_argument("index")))
        aggs=unquote(str(self.get_argument("aggs")))

        r=yield self._bucketize(index, queries, aggs)
        if isinstance(r,str):
            self.set_status(400, str(r))
            return

        self.write(r)
        self.set_status(200,'OK')
        self.finish()
