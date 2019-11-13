#!/usr/bin/python3

from db_ingest import DBIngest
from subprocess import Popen
import requests
import time
import sys
import os

vahost = "http://localhost:8080/pipelines"
mqtthost = os.environ["MQTTHOST"]
dbhost = os.environ["DBHOST"]
every_nth_frame = int(os.environ["EVERY_NTH_FRAME"])
office = list(map(float, os.environ["OFFICE"].split(",")))

class RunVA(object):
    def __init__(self):
        super(RunVA,self).__init__()
        # remove HTTP_PROXY
        env=os.environ.copy()
        env.pop("http_proxy",None)
        env.pop("HTTP_PROXY",None)
        self._va=Popen(["/usr/bin/python3","-m","openapi_server"],cwd="/home/video-analytics/app/server",env=env)
        self._db=DBIngest(host=dbhost, index="algorithms", office=office)
        self._stop=None

    def stop(self):
        self._stop=True

    def loop(self, sensor, location, uri, algorithm, topic):
        req={
            "source": {
                "uri": uri,
                "type":"uri"
            },
            "tags": {
                "sensor": sensor,
                "location": location,
                "algorithm": algorithm,
                "office": {
                    "lat": office[0],
                    "lon": office[1],
                },
            },
            "parameters": {
                "every-nth-frame": every_nth_frame,
                "recording_prefix": "/tmp/" + sensor,
                "method": "mqtt",
                "address": mqtthost,
                "clientid": algorithm,
                "topic": topic,
            },
        }

        while True:
            try:
                r = requests.post(vahost+"/people_counting/2", json=req, timeout=10)
                if r.status_code==200: 
                    pid=int(r.text)
                    break
            except Exception as e:
                print("Exception in runva requests.post: "+str(e), flush=True)
            time.sleep(10)

        while not self._stop:
            r=requests.get(vahost+"/people_counting/2/"+str(pid)+"/status", timeout=10)
            if r.status_code!=200: 
                print("pipeline status: "+str(r.status_code), flush=True)
                print(r.text, flush=True)
                break

            pinfo=r.json()
            print(pinfo, flush=True)

            state = pinfo["state"]
            if state == "COMPLETED" or state == "ABORTED" or state == "ERROR":
                print("pineline ended with "+str(state),flush=True)
                break

            if state == "RUNNING":
                if "avg_pipeline_latency" not in pinfo: pinfo["avg_pipeline_latency"]=0
                self._db.update(algorithm, {
                    "sensor": sensor,
                    "performance": pinfo["avg_fps"], 
                    "latency": pinfo["avg_pipeline_latency"]*1000,
                })
            time.sleep(10)

        print("exiting va pipeline",flush=True)
        self._va.terminate()
