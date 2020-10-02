#!/usr/bin/python3

from tornado import ioloop, web
from tornado.options import define, options, parse_command_line
from auth import AuthHandler
from signal import signal, SIGTERM, SIGQUIT
from configuration import env
from redirect import NGINXRedirect
import json

scenario=env["SCENARIO"]
gwhost=env["GWHOST"]
nginxc=NGINXRedirect(upstreams=[
    ("cloud",gwhost.partition("://")[2])
])

def setup_scenarios():
    with open("/var/www/html/js/scenario.js","at") as fd:
        fd.write("scenarios.setting="+json.dumps(scenario.split(","))+";")

tornado1=None

def quit_service(signum, frame):
    if tornado1: tornado1.add_callback(tornado1.stop)
    nginxc.stop()
        
signal(SIGTERM, quit_service)
setup_scenarios()

app = web.Application([
    (r'/api/auth',AuthHandler),
])

define("port", default=2222, help="the binding port", type=int)
define("ip", default="127.0.0.1", help="the binding ip")
parse_command_line()
print("Listening to " + options.ip + ":" + str(options.port))
app.listen(options.port, address=options.ip)

tornado1=ioloop.IOLoop.instance();
nginxc.start()
tornado1.start()
nginxc.stop()
