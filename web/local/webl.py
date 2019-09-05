#!/usr/bin/python3

from tornado import ioloop, web
from tornado.options import define, options, parse_command_line
from workload import WorkloadHandler
from db_ingest import DBIngest
from subprocess import Popen
from signal import signal, SIGTERM, SIGQUIT
import socket
import os
import time

dbhost=os.environ["DBHOST"]
office=list(map(float,os.environ["OFFICE"].split(",")))
host=os.environ["PROXYHOST"] if "PROXYHOST" in os.environ else "http://"+socket.gethostname()+":8080"

tornadol=None
nginxl=None

def register_office():
    global db,r
    db=DBIngest(index="offices",office="",host=dbhost)
    while True: 
        try:
            r=db.ingest({
                "office": { 
                "lat": office[0],
                "lon": office[1],
                },
                "uri": host,
            },"$".join(map(str,office)))
            return
        except Exception as e:
            print("Exception: "+str(e), flush=True)
            time.sleep(10)

def unregister_office():
    db.delete(r["_id"])

def quit_service(signum, frame):
    if tornadol: tornadol.add_callback(tornadol.stop)
    if nginxl: nginxl.send_signal(SIGQUIT)

app = web.Application([
    (r'/api/workload',WorkloadHandler),
])

if __name__ == "__main__":
    signal(SIGTERM, quit_service)
    register_office()

    define("port", default=2222, help="the binding port", type=int)
    define("ip", default="127.0.0.1", help="the binding ip")
    parse_command_line()
    print("Listening to " + options.ip + ":" + str(options.port))
    app.listen(options.port, address=options.ip)

    tornadol=ioloop.IOLoop.instance();
    nginxl=Popen(["/usr/sbin/nginx"])
    
    tornadol.start()
    nginxl.wait()

    unregister_office()
