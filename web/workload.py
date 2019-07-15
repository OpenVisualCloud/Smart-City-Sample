#!/usr/bin/python3

from tornado import websocket, gen, ioloop
import datetime
import time
import psutil

class WorkloadHandler(websocket.WebSocketHandler):
    def __init__(self, app, request, **kwargs):
        super(WorkloadHandler, self).__init__(app, request, **kwargs)

    def check_origin(self, origin):
        return True

    def data_received(self, chunk):
        pass

    def open(self):
        self.set_nodelay(True)
        ioloop.IOLoop.current().spawn_callback(self._send_workloads)

    @gen.coroutine
    def _send_workloads(self):
        while True:
            yield self.write_message({
                "time": int(time.mktime(datetime.datetime.now().timetuple())*1000),
                "cpu": psutil.cpu_percent(),
                "memory": psutil.virtual_memory(),
                "disk": psutil.disk_usage("/mnt/storage"),
            })
            yield gen.sleep(1)
