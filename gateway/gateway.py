#!/usr/bin/python3

from tornado import ioloop, web
from tornado.options import define, options, parse_command_line
from search import SearchHandler
from histogram import HistogramHandler
from hint import HintHandler
from stats import StatsHandler
from subprocess import Popen
from signal import signal, SIGTERM, SIGQUIT
from threading import Event
from configuration import env
import requests
import time

stHost=env["STHOST"]
tornado1=None
nginx1=None
stop=Event()

def quit_service(signum, frame):
    stop.set()
    if tornado1: tornado1.add_callback(tornado1.stop)
    if nginx1: nginx1.send_signal(SIGQUIT)

def setup_nginx_upstream():
    while True:
        if stop.is_set(): exit(143)
        try:
            r=requests.get(stHost+"/api/workload")
            r.raise_for_status()
            break
        except:
            print("Wait for upstream...", flush=True)
            time.sleep(2)
            continue

    with open("/etc/nginx/upstream.conf","wt") as fd:
        fd.write("upstream storage-service { server "+stHost.partition("://")[2]+"; }")

app = web.Application([
    (r'/api/search',SearchHandler),
    (r'/api/histogram',HistogramHandler),
    (r'/api/hint',HintHandler),
    (r'/api/stats',StatsHandler),
])

if __name__ == "__main__":
    signal(SIGTERM, quit_service)
    setup_nginx_upstream()

    define("port", default=2222, help="the binding port", type=int)
    define("ip", default="127.0.0.1", help="the binding ip")
    parse_command_line()
    print("Listening to " + options.ip + ":" + str(options.port))
    app.listen(options.port, address=options.ip)

    tornado1=ioloop.IOLoop.instance();
    nginx1=Popen(["/usr/local/sbin/nginx"])
    
    tornado1.start()
    nginx1.wait()
