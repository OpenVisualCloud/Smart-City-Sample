#!/usr/bin/python3

from db_query import DBQuery
import time
import os

retention_time=float(os.environ["RETENTION_TIME"])  # in seconds
service_interval=float(os.environ["SERVICE_INTERVAL"])  # in seconds
indexes=os.environ["INDEXES"].split(",")

while True:
    time.sleep(service_interval)

    print("Searching...",flush=True)
    for index in indexes:
        db=DBQuery(index)
        for r in db.search("time<now-"+str(retention_time*1000)):
            # delete the record
            db.delete(r["_id"])

            # delete the path file
            if "path" in r["_source"]:
                try:
                    os.remove(r["_source"]["path"])
                except Exception as e:
                    print(str(e))

