#!/usr/bin/python3

from db_ingest import DBIngest
from db_query import DBQuery
import datetime
import time
import os

service_interval=float(os.environ["SERVICE_INTERVAL"])
office=list(map(float, os.environ["OFFICE"].split(",")))
dbhost=os.environ["DBHOST"]

# register trigger
dbt=DBIngest(index="triggers",office=office,host=dbhost)
rt=dbt.ingest({
    "name": "health_check",
    "status": "idle",
})
print(rt,flush=True)

dbs=DBQuery(index="sensors",office=office,host=dbhost)
dba=DBQuery(index="algorithms",office=office,host=dbhost)
dbat=DBIngest(index="alerts",office=office,host=dbhost)
    
try:
    dbt.update(rt["_id"], { "status": "processing" })

    while True:
        
        try:
            # count #sensors
            nsensors={
                "total": dbs.count("sensor:*"),
                "streaming": dbs.count("status:'streaming'"),
                "idle": dbs.count("status:'idle'"),
            }
            print("nsensors",flush=True)
            print(nsensors,flush=True)

            nalgorithms={
                "total": dba.count("name:*"),
            }
            print("nalgorithms",flush=True)
            print(nalgorithms,flush=True)

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
                print(alerts,flush=True)
                dbat.ingest(alerts)

            time.sleep(service_interval)

        except Exception as e:
            print("Exception "+str(e),flush=True)
            time.sleep(30)

except Exception as e:
    print("Exception: "+str(e),flush=True)
   
# unregister trigger
print(rt,flush=True)
dbt.delete(rt["_id"])
