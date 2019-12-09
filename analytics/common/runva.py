#!/usr/bin/python3

from db_ingest import DBIngest
from modules.PipelineManager import PipelineManager
from modules.ModelManager import ModelManager
from concurrent.futures import ThreadPoolExecutor
from gi.repository import GObject
import time
import os

mqtthost = os.environ["MQTTHOST"]
dbhost = os.environ["DBHOST"]
every_nth_frame = int(os.environ["EVERY_NTH_FRAME"])
office = list(map(float, os.environ["OFFICE"].split(",")))

class RunVA(object):
    def __init__(self, pipeline, version="2"):
        super(RunVA,self).__init__()
        self._pipeline=pipeline
        self._version=version
        self._db=DBIngest(host=dbhost, index="algorithms", office=office)
        self._stop=None

    def stop(self):
        self._stop=True

    def _loop(self, sensor, location, uri, algorithm, topic):
        ModelManager.load_config("/home/models",{})
        PipelineManager.load_config("/home/pipelines",1)

        pid,msg=PipelineManager.create_instance(self._pipeline,self._version,{
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
            "destination": {
                "type": "mqtt",
                "host": mqtthost,
                "clientid": algorithm,
                "topic": topic,
            },
            "parameters": {
                "every-nth-frame": every_nth_frame,
                "recording_prefix": "/tmp/" + sensor,
            },
        })
        if pid is None:
            print("Exception: "+str(msg), flush=True)
            return

        while not self._stop:
            pinfo=PipelineManager.get_instance_status(self._pipeline,self._version,pid)
            if pinfo is not None: 
                print(pinfo, flush=True)
                state = pinfo["state"]
                if state == "COMPLETED" or state == "ABORTED" or state == "ERROR":
                    print("pineline ended with "+str(state),flush=True)
                    break

                if pinfo["avg_fps"]>0:
                    if "avg_pipeline_latency" not in pinfo: pinfo["avg_pipeline_latency"]=0
                    self._db.update(algorithm, {
                        "sensor": sensor,
                        "performance": pinfo["avg_fps"], 
                        "latency": pinfo["avg_pipeline_latency"]*1000,
                    })
            time.sleep(10)

        print("exiting va pipeline",flush=True)
        PipelineManager.stop_instance(self._pipeline,self._version,pid)

    def _mainloop(self):
        try:
            self._ml=GObject.MainLoop()
            self._ml.run()
        except Exception as e:
            print("Exception: "+str(e), flush=True)

    def loop(self, sensor, location, uri, algorithm, topic):
        with ThreadPoolExecutor(1) as e:
            self._ml=None
            e.submit(self._mainloop)
            self._loop(sensor, location, uri, algorithm, topic)
            if self._ml: self._ml.quit()
