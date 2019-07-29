#!/usr/bin/python3

from db_ingest import DBIngest
from db_query import DBQuery
from signal import SIGTERM, signal
import datetime
import time
import os

service_interval=float(os.environ["SERVICE_INTERVAL"])
office=list(map(float, os.environ["OFFICE"].split(",")))
dbhost=os.environ["DBHOST"]

dbt=None
rt=None

def quit_service(signum, sigframe):
    try:
        if dbt and rt: dbt.delete(rt["_id"])
    except Exception as e:
        pass
    exit(143)

signal(SIGTERM, quit_service)

# register trigger
dbt=DBIngest(index="triggers",office=office,host=dbhost)
while True:
    try:
        rt=dbt.ingest({
            "name": "health_check",
            "status": "processing",
        })
        break
    except Exception as e:
        print("Exception: "+str(e), flush=True)
        time.sleep(10)

dbs=DBQuery(index="sensors",office=office,host=dbhost)
dba=DBQuery(index="algorithms",office=office,host=dbhost)
dbat=DBIngest(index="alerts",office=office,host=dbhost)
    
while True:
    try:
        nsensors={
            "total": dbs.count("sensor:*"),
            "streaming": dbs.count("status:'streaming'"),
            "idle": dbs.count("status:'idle'"),
        }
        nalgorithms={
            "total": dba.count("name:*"),
        }
   
        alerts={}
        if nsensors["total"]>nsensors["streaming"]+nsensors["idle"]:
            alerts["maintenance_required"]=nsensors

        if nalgorithms["total"]!=nsensors["streaming"]+nsensors["idle"]:
            alerts["balancing_required"]={
                "nalgorithms": nalgorithms["total"],
                "nsensors": nsensors["streaming"]+nsensors["idle"],
            }

        # ingest alerts
        if alerts:
            alerts["time"]=int(time.mktime(datetime.datetime.now().timetuple())*1000)
            alerts["trigger"]=rt["_id"]
            dbat.ingest(alerts)

    except Exception as e:
        print("Exception "+str(e),flush=True)

    time.sleep(service_interval)
