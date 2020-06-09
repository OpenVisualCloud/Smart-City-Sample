#!/usr/bin/python3

import os
from paho.mqtt.client import Client
from db_ingest import DBIngest
from threading import Event
from vaserving.vaserving import VAServing
from vaserving.pipeline import Pipeline
import time
import traceback
import psutil

mqtthost = os.environ["MQTTHOST"]
dbhost = os.environ["DBHOST"]
every_nth_frame = int(os.environ["EVERY_NTH_FRAME"])
office = list(map(float, os.environ["OFFICE"].split(",")))

class RunVA(object):
    def _test_mqtt_connection(self):
        print("testing mqtt connection", flush=True)
        mqtt = Client()
        while True:
            try:
                mqtt.connect(mqtthost)
                break
            except:
                print("Waiting for mqtt...", flush=True)
                time.sleep(5)
        print("mqtt connected", flush=True)
        mqtt.disconnect()
    
    def __init__(self, pipeline, version="2"):
        super(RunVA, self).__init__()
        self._test_mqtt_connection()

        self._pipeline = pipeline
        self._version = version
        self._db = DBIngest(host=dbhost, index="algorithms", office=office)
        self._stop=None


    def stop(self):
        if self._stop: 
            print("stopping", flush=True)
            self._stop.set()

    def loop(self, sensor, location, uri, algorithm, algorithmName, options={}, topic="analytics"):
        try:
            VAServing.start({
                'model_dir': '/home/models',
                'pipeline_dir': '/home/pipelines',
                'max_running_pipelines': 1,
            })

            try:
                source={
                    "type": "uri",
                    "uri": uri,
                }
                destination={
                    "type": "mqtt",
                    "host": mqtthost,
                    "clientid": algorithm,
                    "topic": topic
                }
                tags={
                    "sensor": sensor, 
                    "location": location, 
                    "algorithm": algorithmName,
                    "office": {
                        "lat": office[0], 
                        "lon": office[1]
                    },
                }
                parameters = {
                    "inference-interval": every_nth_frame,
                    "recording_prefix": "/tmp/rec/" + sensor
                }
                parameters.update(options)

                pipeline = VAServing.pipeline(self._pipeline, self._version)
                instance_id = pipeline.start(source=source,
                                         destination=destination,
                                         tags=tags,
                                         parameters=parameters)

                if instance_id is None:
                    raise Exception("Pipeline {} version {} Failed to Start".format(
                        self._pipeline, self._version))

                self._stop=Event()
                while not self._stop.is_set():
                    status = pipeline.status()
                    print(status, flush=True)

                    if status.state.stopped():
                        print("Pipeline {} Version {} Instance {} Ended with {}".format(
                            self._pipeline, self._version, instance_id, status.state.name), 
                            flush=True)
                        break

                    if status.avg_fps > 0 and status.state is Pipeline.State.RUNNING:
                        avg_pipeline_latency = status.avg_pipeline_latency
                        if not avg_pipeline_latency: avg_pipeline_latency = 0

                        self._db.update(algorithm, {
                            "sensor": sensor,
                            "performance": status.avg_fps,
                            "latency": avg_pipeline_latency * 1000,
                            "cpu": psutil.cpu_percent(),
                            "memory": psutil.virtual_memory().percent,
                        })

                    self._stop.wait(3)

                self._stop=None
                pipeline.stop()
            except:
                print(traceback.format_exc(), flush=True)

            VAServing.stop()
        except:
            print(traceback.format_exc(), flush=True)
