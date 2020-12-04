#!/usr/bin/python3

from db_ingest import DBIngest
from db_query import DBQuery
from signal import signal, SIGTERM
from language import text
from threading import Event
from configuration import env
import os

retention_time=float(env["RETENTION_TIME"])  # in seconds
service_interval=float(env["SERVICE_INTERVAL"])  # in seconds
indexes=env["INDEXES"].split(",")
office=list(map(float, env["OFFICE"].split(","))) if "OFFICE" in env else ""
dbhost=env["DBHOST"]
storage="/var/www/mp4"

stop=Event()
def quit_service(signum, sigframe):
    stop.set()

signal(SIGTERM, quit_service)
dbs=DBIngest(index="services",office=office,host=dbhost)
rs=None
if isinstance(office,list):
    dbs.wait(stop)
    rs=dbs.ingest({
        "name": text["cleanup"],
        "service": text["maintenance"],
        "status": "active",
    })

while not stop.is_set(): 
    print("Searching...",flush=True)
    for index in indexes:
        if stop.is_set(): break

        db=DBQuery(index=index,office=office,host=dbhost)
        try:
            for r in db.search("time<now-"+str(retention_time*1000), size=500):
                if stop.is_set(): break

                # delete the record
                db.delete(r["_id"])
    
                # delete the path file
                if "path" in r["_source"]:
                    try:
                        os.remove(storage+"/"+r["_source"]["path"])
                        os.remove(storage+"/"+r["_source"]["path"]+".png")
                    except Exception as e:
                        pass
        except Exception as e:
            print("Exception: "+str(e), flush=True)

    stop.wait(service_interval)

if rs:
    dbs.delete(rs["_id"])
