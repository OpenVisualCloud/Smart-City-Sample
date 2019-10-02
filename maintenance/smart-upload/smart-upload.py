#!/usr/bin/python3

from db_ingest import DBIngest
from db_query import DBQuery
from signal import signal, SIGTERM
import requests
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
smhost=os.environ["SMHOST"]
cloudhost=os.environ["CLOUDHOST"]

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
        for q in dbq.search(query):
            filename=smhost+'/'+q["_source"]["path"]
            print("filename: ", filename)

            r=requests.head(filename, timeout=10)
            if r.status_code!=200: 
                print("pipeline status: "+str(r.status_code), flush=True)
                print(r.text, flush=True)
                break

            #add updates to request
            print("get url: ", r.url)
            print("send to cloud storage: ", cloudhost)
            print("office: ", str(office[0])+","+str(office[1]))
            #print("sensor: ", sensor)
            #print("year: ", year)
            #print("month: ", month)
            #print("day: ", day)
            #print("time: ", str((os.path.basename(filename).split('.')[0]))
            # r=requests.post(cloudhost,data={
                # "office":str(office[0])+","+str(office[1]),
                # "sensor":***,
                # "year":***, 
                # "month":***,
                # "day":***,
                # "time":str((os.path.basename(filename).split('.')[0])),
                # })

    except Exception as e:
        print("Exception: "+str(e), flush=True)