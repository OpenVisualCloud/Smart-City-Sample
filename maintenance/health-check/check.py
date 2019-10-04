#!/usr/bin/python3

from db_ingest import DBIngest
from db_query import DBQuery
from signal import SIGTERM, signal
import datetime
import psutil
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
dbt=DBIngest(index="services",office=office,host=dbhost)
while True:
    try:
        rt=dbt.ingest({
            "name": "health_check",
            "service": "trigger",
            "status": "active",
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
   
        infos=[]
        warnings=[]
        if nsensors["total"]>nsensors["streaming"]+nsensors["idle"]:
            warnings.append({ 
                "message": "Camera servicing required",
                "args": nsensors,
            })

        if nalgorithms["total"]!=nsensors["streaming"]+nsensors["idle"]:
            infos.append({
                "message": "Analytics balancing required",
                "args": {
                    "nalgorithms": nalgorithms["total"],
                    "nsensors": nsensors["streaming"]+nsensors["idle"],
                },
            })

        fatals=[]
        # check CPU utilization
        workload={
            "args": {
                "cpu": psutil.cpu_percent(),
            },
        }
        if workload["args"]["cpu"]>90:
            workload["message"]="Server overload: "+str(workload["args"]["cpu"])+"%"
            fatals.append(workload)
        elif workload["args"]["cpu"]>80:
            workload["message"]="Server busy: "+str(workload["args"]["cpu"])+"%"
            warnings.append(workload)

        # ingest alerts
        if infos or warnings or fatals:
            dbat.ingest({
                "location": {
                    "lat": office[0],
                    "lon": office[1],
                },
                "office": {
                    "lat": office[0],
                    "lon": office[1],
                },
                "time": int(time.mktime(datetime.datetime.now().timetuple())*1000),
                "warning": warnings,
                "fatal": fatals,
                "info": infos,
            })

    except Exception as e:
        print("Exception "+str(e),flush=True)

    time.sleep(service_interval)
