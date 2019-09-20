#!/usr/bin/python3

from db_ingest import DBIngest
from db_query import DBQuery
from signal import signal, SIGTERM
import os
import time

query=os.environ["QUERY"]
indexes=os.environ["INDEXES"]
service_interval=float(os.environ["SERVICE_INTERVAL"])  # in seconds
update_interval=float(os.environ["UPDATE_INTERVAL"])  # in seconds
search_batch=int(os.environ["SEARCH_BATCH"])
update_batch=int(os.environ["UPDATE_BATCH"])
office=list(map(float, os.environ["OFFICE"].split(",")))
dbhost=os.environ["DBHOST"]

def quit_service(signum, sigframe):
    if dbs and rs: dbs.delete(rs["_id"])
    exit(143)

signal(SIGTERM, quit_service)
dbs=DBIngest(index="services",office=office,host=dbhost)
while True:
    try:
        dbs.ingest({
            "name": "smart-upload",
            "service": "maintanence",
            "status": "active",
        })
        break
    except Exception as e:
        print("Exception: "+str(e), flush=True)
        time.sleep(10)

dbq=DBQuery(index=indexes,office=office,host=dbhost)

while True:
    print("Sleeping...")
    time.sleep(service_interval)

    print("Searching...",flush=True)
    print("query = ", query)

    try:
        updates=[]
        for q in dbq.search(query):
            updates.append({"recording":q["_source"]["path"]})
            print(q["_source"]["path"])
        if updates:
            print("update "+str(len(updates)))

    except Exception as e:
        print("Exception: "+str(e), flush=True)
