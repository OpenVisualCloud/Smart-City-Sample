#!/usr/bin/python3

from db_ingest import DBIngest
from signal import signal,SIGTERM
from subprocess import Popen
import requests
import time
import sys
import os

if len(sys.argv)<5:
    print("Usage: <sensor> <uri> <algorithm> <topic>")
    exit(-1)

vahost = "http://localhost:8080/pipelines"
mqtthost = os.environ["MQTTHOST"]
dbhost = os.environ["DBHOST"]
every_nth_frame = int(os.environ["EVERY_NTH_FRAME"])
office = list(map(float, os.environ["OFFICE"].split(",")))

stop=False
va=None

def quit_service(signum, sigframe):
    global stop, va
    if va: va.kill()
    stop=True

sensor=sys.argv[1]
uri=sys.argv[2]
algorithm=sys.argv[3]
topic=sys.argv[4]

db=DBIngest(host=dbhost, index="algorithms", office=office)
va=Popen(["/usr/bin/python3","-m","openapi_server"],cwd="/home/video-analytics/app/server")

req={
    "source": {
        "uri": uri,
        "type":"uri"
    },
    "tags": {
        "sensor": sensor,
        "algorithm": algorithm,
    },
    "parameters": {
        "every-nth-frame": every_nth_frame,
        "recording_prefix": "recordings/" + sensor,
        "method": "mqtt",
        "address": mqtthost,
        "clientid": algorithm,
        "topic": topic,
    },
}

while True:
    try:
        print(vahost+"/object_detection/2",flush=True)
        r = requests.post(vahost+"/object_detection/2", json=req, timeout=10)
        if r.status_code==200: break
    except Exception as e:
        print("Exception: "+str(e), flush=True)
    time.sleep(10)

print("pid: "+r.text, flush=True)
pid=int(r.text)
while r.status_code==200 and not stop:
    r=requests.get(vahost+"/object_detection/2/"+str(pid)+"/status", timeout=10)
    r.raise_for_status()
    pinfo=r.json()
    if "avg_pipeline_latency" not in pinfo: pinfo["avg_pipeline_latency"]=0
    print(pinfo, flush=True)

    state = pinfo["state"]
    if state == "COMPLETED" or state == "ABORTED" or state == "ERROR":
        print("pineline ended with "+str(state),flush=True)
        break

    db.update(algorithm, {
        "performance": pinfo["avg_fps"], 
        "latency": pinfo["avg_pipeline_latency"]*1000,
    })
    time.sleep(2)

print("exiting va pipeline",flush=True)
va.kill()
va.wait()
