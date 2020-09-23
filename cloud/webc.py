#!/usr/bin/python3

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

def quit_service(signum, frame):
    nginxc.stop()
        
signal(SIGTERM, quit_service)
setup_scenarios()

nginxc.start()
nginxc.wait()
nginxc.stop()
