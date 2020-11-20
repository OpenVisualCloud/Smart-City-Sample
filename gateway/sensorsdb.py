#!/usr/bin/python3

from urllib.parse import unquote
from tornado import web,gen
from tornado.concurrent import run_on_executor
from concurrent.futures import ThreadPoolExecutor
from db_query import DBQuery
from db_ingest import DBIngest
from language import encode
from configuration import env
import json

dbhost=env["DBHOST"]
office=list(map(float,env["OFFICE"].split(","))) if "OFFICE" in env else ""

class SensorsDBHandler(web.RequestHandler):
    def __init__(self, app, request, **kwargs):
        super(SensorsDBHandler, self).__init__(app, request, **kwargs)
        self.executor= ThreadPoolExecutor(4)
        self._dbi=DBIngest(index="sensors",office=office,host=dbhost)

    def check_origin(self, origin):
        return True

    @run_on_executor
    def _update(self, sensor, source):
        try:
            print("Ingesting", sensor, flush=True)
            r=self._dbi.ingest(source, refresh="wait_for")
            return r
        except Exception as e:
            print(str(e),flush=True)
            return str(e)

    @gen.coroutine
    def put(self):
        options=json.loads(self.request.body.decode('utf-8'))
        r=yield self._update(sensor=options["sensor"], source=options["source"])
        if isinstance(r,str):
            self.set_status(400, encode(r))
            return

        self.write(r)
        self.set_status(200,'OK')
        self.finish()
