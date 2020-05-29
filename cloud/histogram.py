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

class HistogramHandler(web.RequestHandler):
    def __init__(self, app, request, **kwargs):
        super(HistogramHandler, self).__init__(app, request, **kwargs)
        self.executor= ThreadPoolExecutor(8)

    def check_origin(self, origin):
        return True

    @run_on_executor
    def _bucketize(self, index, queries, field, size, office):
        db=DBQuery(index=index,office=office,host=dbhost)
        try:
            buckets=db.bucketize(queries, [field], size)
        except Exception as e:
            return str(e)

        # reformat buckets to have str keys
        buckets1={}
        if field in buckets:
            for k in buckets[field]: 
                buckets1[str(k)]=buckets[field][k]
        return buckets1

    @gen.coroutine
    def get(self):
        queries=unquote(str(self.get_argument("queries")))
        index=unquote(str(self.get_argument("index")))
        field=unquote(str(self.get_argument("field")))
        size=int(self.get_argument("size"))
        office=list(map(float,unquote(str(self.get_argument("office"))).split(",")))

        r=yield self._bucketize(index, queries, field, size, office)
        if isinstance(r,str):
            self.set_status(400, encode(r))
            return

        self.write(r)
        self.set_status(200,'OK')
        self.finish()
