#!/usr/bin/python3

from tornado import ioloop, web
from tornado.options import define, options, parse_command_line
from workload import WorkloadHandler
from upload import UploadHandler
from thumbnail import ThumbnailHandler
from subprocess import Popen
from signal import signal, SIGTERM, SIGQUIT
import os
import time

tornado1=None
nginx1=None
cleanup1=None

def quit_service(signum, frame):
    if tornado1: tornado1.add_callback(tornado1.stop)
    if nginx1: nginx1.send_signal(SIGQUIT)
    if cleanup1: cleanup1.send_signal(SIGTERM)

app = web.Application([
    (r'/api/workload',WorkloadHandler),
    (r'/api/upload',UploadHandler),
    (r'/api/thumbnail/.*',ThumbnailHandler),
])

if __name__ == "__main__":
    signal(SIGTERM, quit_service)

    define("port", default=2222, help="the binding port", type=int)
    define("ip", default="127.0.0.1", help="the binding ip")
    parse_command_line()
    print("Listening to " + options.ip + ":" + str(options.port))
    app.listen(options.port, address=options.ip)

    tornado1=ioloop.IOLoop.instance();
    nginx1=Popen(["/usr/local/sbin/nginx"])
    cleanup1=Popen(["/home/cleanup.py"])
    
    tornado1.start()
    cleanup1.wait()
    nginx1.wait()
