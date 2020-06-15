#!/usr/bin/python3

from db_ingest import DBIngest
from signal import SIGTERM, signal
from concurrent.futures import ThreadPoolExecutor
from cpu_trigger import CPUTrigger
from imbalance_trigger import ImbalanceTrigger
from occupency_trigger import OccupencyTrigger
from language import text
import time
import os

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
            "name": text["alert trigger"],
            "service": text["triggers"],
            "status": "active",
        })
        break
    except Exception as e:
        print("Waiting for DB...", flush=True)
        time.sleep(10)

imbalance=ImbalanceTrigger()
occupency=OccupencyTrigger()
cpu=CPUTrigger()
with ThreadPoolExecutor(3) as e:
    e.submit(imbalance.loop)
    e.submit(occupency.loop)
    e.submit(cpu.loop)

