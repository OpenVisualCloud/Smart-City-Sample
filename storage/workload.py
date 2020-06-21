#!/usr/bin/python3

from tornado import web, gen
from tornado.concurrent import run_on_executor
from concurrent.futures import ThreadPoolExecutor
from urllib.parse import unquote
import time
import psutil
import os

class WorkloadHandler(web.RequestHandler):
    def __init__(self, app, request, **kwargs):
        super(WorkloadHandler, self).__init__(app, request, **kwargs)
        self.executor= ThreadPoolExecutor(4)

    def check_origin(self, origin):
        return True

    @run_on_executor
    def _workload(self):
        return {
            "time": int(time.time()*1000),
            "cpu": psutil.cpu_percent(),
            "memory": psutil.virtual_memory().percent,
            "disk": psutil.disk_usage("/var/www/mp4").percent,
        }

    @gen.coroutine
    def get(self):
        workload=yield self._workload()
        self.write(workload)
        self.set_status(200,'OK')
