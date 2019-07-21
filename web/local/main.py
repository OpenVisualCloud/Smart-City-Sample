#!/usr/bin/python3

from tornado import ioloop, web
from tornado.options import define, options, parse_command_line
from workload import WorkloadHandler
from db_ingest import DBIngest
import socket
import os

app = web.Application([
    (r'/api/workload',WorkloadHandler),
])

if __name__ == "__main__":
    dbhost=os.environ["DBHOST"]
    office=list(map(float,os.environ["OFFICE"].split(",")))
    hostname=socket.gethostbyname(socket.gethostname())
    
    db=DBIngest(index="offices",office="",host=dbhost)
    r=db.ingest({
       "office": { 
           "lat": office[0],
           "lon": office[1],
       },
       "uri": "http://"+hostname+":8080",
    },"$".join(map(str,office)))

    define("port", default=2222, help="the binding port", type=int)
    define("ip", default="127.0.0.1", help="the binding ip")
    parse_command_line()
    print("Listening to " + options.ip + ":" + str(options.port))

    app.listen(options.port, address=options.ip)
    ioloop.IOLoop.instance().start()
