#!/usr/bin/python3

from db_ingest import DBIngest
from db_query import DBQuery
from signal import signal, SIGTERM
from language import text
import os
import time

service_interval=float(os.environ["SERVICE_INTERVAL"])  # in seconds
update_interval=float(os.environ["UPDATE_INTERVAL"])  # in seconds
search_batch=int(os.environ["SEARCH_BATCH"])
update_batch=int(os.environ["UPDATE_BATCH"])
office=list(map(float, os.environ["OFFICE"].split(","))) if "OFFICE" in os.environ else ""
dbhost=os.environ["DBHOST"]

dbs=None
rs=None

def quit_service(signum, sigframe):
    if dbs and rs: dbs.delete(rs["_id"])
    exit(143)

signal(SIGTERM, quit_service)
dbs=DBIngest(index="services",office=office,host=dbhost)
while True:
    try:
        dbs.ingest({
            "name": text["where-indexing"],
            "service": text["maintanence"],
            "status": "active",
        })
        break
    except Exception as e:
        print("Waiting for DB...", flush=True)
        time.sleep(10)

dbq=DBQuery(index="recordings",office=office,host=dbhost)
dba=DBQuery(index="analytics",office=office,host=dbhost)
while True:
    print("Sleeping...")
    time.sleep(service_interval)

    print("Searching...",flush=True)
    try:
        data=list(dba.search("not recording=*", size=search_batch))
        if not data: continue

        updates=[]
        while data:
            sensor1=data[-1]["_source"]["sensor"]
            office1=data[-1]["_source"]["office"]
            time1=data[-1]["_source"]["time"]

            for q in dbq.search('sensor="'+sensor1+'" and office:['+str(office1["lat"])+','+str(office1["lon"])+'] and time<='+str(time1)+' and time+duration*1000>='+str(time1)):
                for i in range(len(data)-1,-1,-1):
                    if data[i]["_source"]["sensor"]==sensor1 and data[i]["_source"]["office"]==office1 and data[i]["_source"]["time"]>=q["_source"]["time"] and data[i]["_source"]["time"]<=q["_source"]["time"]+q["_source"]["duration"]*1000:
                        updates.append([data[i]["_id"],{"recording":q["_id"]}])
                        del data[i]
                        if len(updates)>=update_batch:
                            print("update "+str(update_batch))
                            dba.update_bulk(updates)
                            time.sleep(update_interval)
                            updates=[]

        if updates:
            print("update "+str(len(updates)))
            dba.update_bulk(updates)
            time.sleep(update_interval)
    except Exception as e:
        print("Exception: "+str(e), flush=True)
