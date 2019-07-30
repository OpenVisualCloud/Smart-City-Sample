#!/usr/bin/python3

from tornado import ioloop, web
from tornado.options import define, options, parse_command_line
from search import SearchHandler
from hint import HintHandler
from redirect import RedirectHandler
from stats import StatsHandler
from subprocess import Popen
from signal import signal, SIGTERM, SIGQUIT

tornado1=None
nginx1=None

def quit_service(signum, frame):
    if tornado1: tornado1.add_callback(tornado1.stop)
    if nginx1: nginx1.send_signal(SIGQUIT)
        
app = web.Application([
    (r'/api/search',SearchHandler),
    (r'/api/stats',StatsHandler),
    (r'/api/workload',RedirectHandler),
    (r'/api/hint',HintHandler),
    (r'/recording/.*',RedirectHandler),
])

if __name__ == "__main__":
    signal(SIGTERM, quit_service)

    define("port", default=2222, help="the binding port", type=int)
    define("ip", default="127.0.0.1", help="the binding ip")
    parse_command_line()
    print("Listening to " + options.ip + ":" + str(options.port))
    app.listen(options.port, address=options.ip)

    tornado1=ioloop.IOLoop.instance();
    nginx1=Popen(["/usr/sbin/nginx"])
    tornado1.start()
    nginx1.wait()
