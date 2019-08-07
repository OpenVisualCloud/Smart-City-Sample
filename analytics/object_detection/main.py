#!/usr/bin/python3

from db_ingest import DBIngest
from db_query import DBQuery
from signal import signal, SIGTERM
from subprocess import Popen
import os
import time

office = list(map(float, os.environ["OFFICE"].split(",")))
dbhost = os.environ["DBHOST"]
every_nth_frame = int(os.environ["EVERY_NTH_FRAME"])

mqtt2db=None
rec2db=None
va=None
stop=False

def connect(sensor, algorithm, uri):
    global mqtt2db, rec2db, va

    try:
        topic="smtc_va_inferences_"+algorithm
        mqtt2db=Popen(["/home/mqtt2db.py",algorithm,topic])
        rec2db=Popen(["/home/rec2db.py",sensor])
        va=Popen(["/home/runva.py",sensor,uri,algorithm,topic])
        va.wait()

        rec2db.send_signal(SIGTERM)
        mqtt2db.send_signal(SIGTERM)
        rec2db.wait()
        mqtt2db.wait()
    except Exception as e:
        print("Exception: "+str(e), flush=True)

def quit_service(signum, sigframe):
    global stop
    if mqtt2db: mqtt2db.send_signal(SIGTERM)
    if rec2db: rec2db.send_signal(SIGTERM)
    if va: va.send_signal(SIGTERM)
    stop=True

signal(SIGTERM, quit_service)
dba=DBIngest(host=dbhost, index="algorithms", office=office)
dbs=DBQuery(host=dbhost, index="sensors", office=office)

# register algorithm (while waiting for db to startup)
while True:
    try:
        algorithm=dba.ingest({
            "name": "object_detection",
            "office": {
                "lat": office[0],
                "lon": office[1],
            },
            "status": "processing",
            "skip": every_nth_frame,
        })["_id"]
        break
    except Exception as e:
        print("Exception: "+str(e), flush=True)
        time.sleep(10)

# compete for a sensor connection
while not stop:
    try:
        print("Searching...", flush=True)
        for sensor in dbs.search("sensor:'camera' and status:'idle' and office:["+str(office[0])+","+str(office[1])+"]"):
            try:
                # compete (with other va instances) for a sensor
                r=dbs.update(sensor["_id"],{"status":"streaming"},version=sensor["_version"])

                # stream from the sensor
                print("Connected to "+sensor["_id"]+"...",flush=True)
                connect(sensor["_id"],algorithm,sensor["_source"]["url"])

                # if exit, there is somehting wrong
                r=dbs.update(sensor["_id"],{"status":"disconnected"})
                if stop: break

            except Exception as e:
                print("Exception: "+str(e), flush=True)

    except Exception as e:
        print("Exception: "+str(e), flush=True)

    time.sleep(10)

# delete the algorithm instance
dba.delete(algorithm)

