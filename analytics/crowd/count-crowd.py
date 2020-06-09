#!/usr/bin/python3

from db_ingest import DBIngest
from db_query import DBQuery
from signal import signal, SIGTERM
from concurrent.futures import ThreadPoolExecutor
from rec2db import Rec2DB
from runva import RunVA
from language import text
import os
import time
import uuid
import logging

log = logging.getLogger("count-crowd")
log.setLevel(logging.INFO)

office = list(map(float, os.environ["OFFICE"].split(",")))
dbhost = os.environ["DBHOST"]
every_nth_frame = int(os.environ["EVERY_NTH_FRAME"])

runva=None
stop=False

def connect(sensor, location, uri, algorithm, algorithmName, resolution, zonemap):
    global runva

    try:
        rec2db=Rec2DB(sensor)
        runva=RunVA("crowd_counting")

        with ThreadPoolExecutor(2) as e:
            e.submit(rec2db.loop)

            # any VA exit indicates a camera disconnect
            with ThreadPoolExecutor(1) as e1:
                e1.submit(runva.loop, sensor, location, uri, algorithm, algorithmName, {
                    "crowd_count": {
                        "width": resolution["width"],
                        "height": resolution["height"],
                        "zonemap": zonemap,
                    },
                })

            if stop: rec2db.stop()
            raise Exception("VA exited. This should not happen.")

    except Exception as e:
        print("Exception in connect: "+str(e), flush=True)

def quit_service(signum, sigframe):
    global stop
    stop=True
    if runva: runva.stop()

signal(SIGTERM, quit_service)
dba=DBIngest(host=dbhost, index="algorithms", office=office)
dbs=DBQuery(host=dbhost, index="sensors", office=office)

# register algorithm (while waiting for db to startup)
while not stop:
    try:
        algorithm=dba.ingest({
            "name": text["crowd-counting"],
            "office": {
                "lat": office[0],
                "lon": office[1],
            },
            "status": "processing",
            "skip": every_nth_frame,
        })["_id"]
        break
    except Exception as e:
        print("Waiting for DB...", flush=True)
        time.sleep(10)

# compete for a sensor connection
while not stop:
    try:
        print("Searching...", flush=True)
        for sensor in dbs.search("sensor:'camera' and status:'idle' and algorithm='crowd-counting' and office:["+str(office[0])+","+str(office[1])+"]"):
            try:
                # compete (with other va instances) for a sensor
                r=dbs.update(sensor["_id"],{"status":"streaming"},seq_no=sensor["_seq_no"],primary_term=sensor["_primary_term"])

                # stream from the sensor
                print("Connected to "+sensor["_id"]+"...",flush=True)
                connect(sensor["_id"],sensor["_source"]["location"],sensor["_source"]["url"],algorithm,sensor["_source"]["algorithm"],sensor["_source"]["resolution"],sensor["_source"]["zonemap"])

                # if exit, there is somehting wrong
                r=dbs.update(sensor["_id"],{"status":"disconnected"})
                if stop: break

            except Exception as e:
                print("Exception in count-crowd search sensor: "+str(e), flush=True)

    except Exception as e:
        print("Exception in count-crowd sensor connection: "+str(e), flush=True)

    time.sleep(10)

# delete the algorithm instance
dba.delete(algorithm)

