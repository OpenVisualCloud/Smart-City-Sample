#!/usr/bin/python3

from tornado import ioloop, web
from tornado.options import define, options, parse_command_line
from search import SearchHandler
from histogram import HistogramHandler
from hint import HintHandler
from stats import StatsHandler
from sensorsdb import SensorsDBHandler
from signal import signal, SIGTERM, SIGQUIT
from configuration import env
from nginx import NGINX

sthost=env["STHOST"]
dbhost=env["DBHOST"]
webrtchost=env.get("WEBRTCHOST","http://127.0.0.1:8888")
tornado1=None
nginx1=NGINX(upstreams=[
    ("storage-service", sthost.partition("://")[2]),
    ("database-service", dbhost.partition("://")[2]),
    ("webrtc-service", webrtchost.partition("://")[2]),
])

def quit_service(signum, frame):
    if tornado1: tornado1.add_callback(tornado1.stop)
    nginx1.stop()

app = web.Application([
    (r'/api/search',SearchHandler),
    (r'/api/histogram',HistogramHandler),
    (r'/api/hint',HintHandler),
    (r'/api/stats',StatsHandler),
    (r'/api/sensorsdb',SensorsDBHandler),
])

if __name__ == "__main__":
    signal(SIGTERM, quit_service)

    define("port", default=2222, help="the binding port", type=int)
    define("ip", default="127.0.0.1", help="the binding ip")
    parse_command_line()
    print("Listening to " + options.ip + ":" + str(options.port))
    app.listen(options.port, address=options.ip)

    tornado1=ioloop.IOLoop.instance();
    nginx1.start()
    
    tornado1.start()
    nginx1.stop()
