#!/usr/bin/python3

from db_query import DBQuery
from signal import signal, SIGTERM
import os
import time

indexes=os.environ["INDEXES"].split(",")
service_interval=float(os.environ["SERVICE_INTERVAL"])  # in seconds
update_interval=float(os.environ["UPDATE_INTERVAL"])  # in seconds
search_batch=int(os.environ["SEARCH_BATCH"])
update_batch=int(os.environ["UPDATE_BATCH"])
office=list(map(float, os.environ["OFFICE"].split(",")))
dbhost=os.environ["DBHOST"]

def quit_service(signum, sigframe):
    exit(143)

signal(SIGTERM, quit_service)
dbq=DBQuery(index=indexes[0],office=office,host=dbhost)
dba=DBQuery(index=indexes[1],office=office,host=dbhost)
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
