#!/usr/bin/python3

from db_ingest import DBIngest
from db_query import DBQuery
from signal import signal, SIGTERM
import os
import time

record_time=os.environ["RECORD_TIME"]
width_interval=os.environ["WIDTH_INTERVAL"]
indexes=os.environ["INDEXES"]
service_interval=float(os.environ["SERVICE_INTERVAL"])  # in seconds
update_interval=float(os.environ["UPDATE_INTERVAL"])  # in seconds
search_batch=int(os.environ["SEARCH_BATCH"])
update_batch=int(os.environ["UPDATE_BATCH"])
office=list(map(float, os.environ["OFFICE"].split(",")))
dbhost=os.environ["DBHOST"]

dbq=DBQuery(index=indexes,office=office,host=dbhost)

while True:
    print("Sleeping...")
    time.sleep(service_interval)

    print("Searching...",flush=True)
    criteria = 'time>='+record_time+' where objects.detection.bounding_box.x_max-objects.detection.bounding_box.x_min>'+width_interval
    print("criteria = ", criteria)

    try:
        updates=[]
        for q in dbq.search(criteria):
            updates.append({"recording":q["_source"]["path"]})
            print(q["_source"]["path"])
        if updates:
            print("update "+str(len(updates)))

    except Exception as e:
        print("Exception: "+str(e), flush=True)
