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

tornado1=None
nginx1=None

app = web.Application([
    (r'/api/workload',WorkloadHandler),
])

def quit_service(signum, frame):
    if tornado1: tornado1.add_callback(tornado1.stop)
    if nginx1: nginx1.send_signal(SIGQUIT)

if __name__ == "__main__":
    dbhost=os.environ["DBHOST"]
    office=os.environ["OFFICE"].split(",")
    hostname=socket.gethostbyname(socket.gethostname())
    
    signal(SIGTERM, quit_service)

    db=DBIngest(index="offices",office="",host=dbhost)
    while true: 
        try:
            r=db.ingest({
                "office": { 
                "lat": float(office[0]),
                "lon": float(office[1]),
                },
                "uri": "http://"+hostname+":8080",
            },"$".join(office))
            break
        except Exception as e:
            print("Exception: "+str(e), flush=True)
        time.sleep(10)

    define("port", default=2222, help="the binding port", type=int)
    define("ip", default="127.0.0.1", help="the binding ip")
    parse_command_line()
    print("Listening to " + options.ip + ":" + str(options.port))

    app.listen(options.port, address=options.ip)
    tornado1=ioloop.IOLoop.instance();
    nginx1=Popen(["/usr/sbin/nginx"])
    
    tornado1.start()
    nginx1.wait()
    db.delete(r["_id"])
