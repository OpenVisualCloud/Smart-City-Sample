#!/usr/bin/python3

from urllib.parse import unquote
from tornado import web,gen
from tornado.concurrent import run_on_executor
from concurrent.futures import ThreadPoolExecutor
from language import text, encode
from db_query import DBQuery
import os

dbhost=os.environ["DBHOST"]
office=list(map(float,os.environ["OFFICE"].split(","))) if "OFFICE" in os.environ else ""
dbq=DBQuery(index="",office=office,host=dbhost)

class HealthHandler(web.RequestHandler):
    def __init__(self, app, request, **kwargs):
        super(HealthHandler, self).__init__(app, request, **kwargs)
        self.executor= ThreadPoolExecutor(2)

    def check_origin(self, origin):
        return True

    @run_on_executor
    def _check_health(self):
        try:
            if dbq.health(): return { "state": "online" }
            return text["connection error"]
        except Exception as e:
            print("Exception: "+str(e), flush=True)
            return text["connection error"]

    @gen.coroutine
    def get(self):
        r=yield self._check_health()
        if isinstance(r, str):
            self.set_status(400, encode(r))
            return

        self.write({"response":r})
        self.set_status(200, 'OK')
