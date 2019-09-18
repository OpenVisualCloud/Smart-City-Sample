#!/usr/bin/python3

from db_ingest import DBIngest
from signal import signal, SIGTERM
import socket
import time
import os

dbhost=os.environ["DBHOST"]
office=list(map(float,os.environ["OFFICE"].split(","))) if "OFFICE" in os.environ else None
host=os.environ["PROXYHOST"] if "PROXYHOST" in os.environ else "http://"+socket.gethostname()+":8080"

db=DBIngest(index="offices",office="",host=dbhost)
r=None

def quit_service(signum, sigframe):
    if r: db.delete(r["_id"])
    exit(143)

signal(SIGTERM, quit_service)
while office:
    try:
        r=db.ingest({
            "office": {
                "lat": office[0],
                "lon": office[1],
            },
            "uri": host,
        },"$".join(map(str,office)))
        break
    except Exception as e:
        print("Exception: "+str(e), flush=True)
        time.sleep(10)

while office:
    time.sleep(1000)
    
