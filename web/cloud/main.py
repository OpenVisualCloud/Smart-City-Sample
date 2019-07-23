#!/usr/bin/python3

from tornado import ioloop, web
from tornado.options import define, options, parse_command_line
from search import SearchHandler
from hint import HintHandler
from redirect import RedirectHandler
from stats import StatsHandler
from subprocess import Popen
from signal import signal, SIGTERM, SIGQUIT

app = web.Application([
    (r'/api/search',SearchHandler),
    (r'/api/stats',StatsHandler),
    (r'/api/workload',RedirectHandler),
    (r'/api/hint',HintHandler),
    (r'/recording/.*',RedirectHandler),
])

if __name__ == "__main__":
    define("port", default=2222, help="the binding port", type=int)
    define("ip", default="127.0.0.1", help="the binding ip")
    parse_command_line()
    print("Listening to " + options.ip + ":" + str(options.port))
    app.listen(options.port, address=options.ip)

    tornado1=ioloop.IOLoop.instance();
    nginx1=Popen(["/usr/sbin/nginx"])

    # set SIGTERM/SIGQUIT handler
    def quit_nicely(signum, frame):
        nginx1.send_signal(SIGQUIT)
        tornado1.add_callback(tornado1.stop)
        
    signal(SIGTERM, quit_nicely)
    tornado1.start()
    nginx1.wait()
