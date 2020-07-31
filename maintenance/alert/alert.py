#!/usr/bin/python3

from db_ingest import DBIngest
from signal import SIGTERM, signal
from concurrent.futures import ThreadPoolExecutor
from cpu_trigger import CPUTrigger
from imbalance_trigger import ImbalanceTrigger
from occupency_trigger import OccupencyTrigger
from language import text
from threading import Event
import os

office=list(map(float, os.environ["OFFICE"].split(",")))
dbhost=os.environ["DBHOST"]

stop=Event()
def quit_service(signum, sigframe):
    stop.set()

signal(SIGTERM, quit_service)

# register trigger
dbt=DBIngest(index="services",office=office,host=dbhost)
dbt.wait(stop)
rt=dbt.ingest({
    "name": text["alert trigger"],
    "service": text["triggers"],
    "status": "active",
})

imbalance=ImbalanceTrigger()
occupency=OccupencyTrigger()
cpu=CPUTrigger()
with ThreadPoolExecutor(3) as e:
    e.submit(imbalance.loop,stop)
    e.submit(occupency.loop,stop)
    e.submit(cpu.loop,stop)

dbt.delete(rt["_id"])
