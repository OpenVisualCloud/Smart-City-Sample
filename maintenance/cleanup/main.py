#!/usr/bin/python3

from db_query import DBQuery
from signal import signal, SIGTERM
import time
import os

retention_time=float(os.environ["RETENTION_TIME"])  # in seconds
service_interval=float(os.environ["SERVICE_INTERVAL"])  # in seconds
indexes=os.environ["INDEXES"].split(",")
office=list(map(float, os.environ["OFFICE"].split(",")))
dbhost=os.environ["DBHOST"]

def quit_nicely(signum, sigframe):
    exit(143)

# set signal to quit nicely
signal(SIGTERM, quit_nicely)

while True: 
    time.sleep(service_interval)

    print("Searching...",flush=True)
    for index in indexes:
        db=DBQuery(index=index,office=office,host=dbhost)
        for r in db.search("time<now-"+str(retention_time*1000), size=500):
            # delete the record
            db.delete(r["_id"])

            # delete the path file
            if "path" in r["_source"]:
                try:
                    os.remove(r["_source"]["path"])
                except Exception as e:
                    print(str(e))
