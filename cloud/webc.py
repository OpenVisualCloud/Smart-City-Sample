#!/usr/bin/python3

from tornado import ioloop, web
from tornado.options import define, options, parse_command_line
from redirect import RedirectHandler
from signal import signal, SIGTERM, SIGQUIT
from configuration import env
from nginx import NGINX
import json

scenario=env["SCENARIO"]
tornadoc=None
nginxc=NGINX()

def setup_scenarios():
    with open("/var/www/html/js/scenario.js","at") as fd:
        fd.write("scenarios.setting="+json.dumps(scenario.split(","))+";")

def quit_service(signum, frame):
    if tornadoc: tornadoc.add_callback(tornadoc.stop)
    nginxc.stop()
        
app = web.Application([
    (r'/api/search',RedirectHandler),
    (r'/api/stats',RedirectHandler),
    (r'/api/histogram',RedirectHandler),
    (r'/api/workload',RedirectHandler),
    (r'/api/hint',RedirectHandler),
    (r'/recording/.*',RedirectHandler),
    (r'/thumbnail/.*',RedirectHandler),
])

if __name__ == "__main__":
    signal(SIGTERM, quit_service)
    setup_scenarios()

    define("port", default=2222, help="the binding port", type=int)
    define("ip", default="127.0.0.1", help="the binding ip")
    parse_command_line()
    print("Listening to " + options.ip + ":" + str(options.port))
    app.listen(options.port, address=options.ip)

    tornadoc=ioloop.IOLoop.instance();
    nginxc.start()
    tornadoc.start()
    nginxc.stop()
