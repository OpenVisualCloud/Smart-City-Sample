#!/usr/bin/python3

from urllib.parse import unquote
from tornado import web,gen
from tornado.concurrent import run_on_executor
from concurrent.futures import ThreadPoolExecutor
from language import text, encode
import requests
import os
import json

dbhost=os.environ["DBHOST"]
health_check=os.environ["HEALTH_CHECK"]

class HealthHandler(web.RequestHandler):
    def __init__(self, app, request, **kwargs):
        super(HealthHandler, self).__init__(app, request, **kwargs)
        self.executor= ThreadPoolExecutor(2)

    def check_origin(self, origin):
        return True

    @run_on_executor
    def _check_health(self, zone):
        try:
            r=requests.get(dbhost+"/_nodes/"+zone+"/http")
            if r.json()["_nodes"]["successful"]>0: 
                return { "state": "online" }
            return text["connection error"]
        except Exception as e:
            print("Exception: "+str(e), flush=True)
            return text["connection error"]

    @gen.coroutine
    def get(self):
        zone=unquote(str(self.get_argument("zone")))
        if health_check=="enabled":
            r=yield self._check_health(zone)
            if isinstance(r, str):
                self.set_status(400, encode(r))
                return
        else:
            r={ "state": "online" }

        self.write({"response":r})
        self.set_status(200, 'OK')
        self.finish()
