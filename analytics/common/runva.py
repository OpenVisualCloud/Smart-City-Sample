#!/usr/bin/python3

from paho.mqtt.client import Client
from db_ingest import DBIngest
from threading import Event
from vaserving.vaserving import VAServing
from vaserving.pipeline import Pipeline
from configuration import env
from filewatch import FileWatcher
import time
import traceback
import psutil
import ssl

mqtthost = env["MQTTHOST"]
dbhost = env["DBHOST"]
every_nth_frame = int(env["EVERY_NTH_FRAME"])
office = list(map(float, env["OFFICE"].split(",")))

class RunVA(object):
    def _mqtt_connect(self):
        print("mqtt connecting", flush=True)
        
        self._mqtt = Client()
        self._mqtt.tls_set("/run/secrets/self.crt","/run/secrets/mqtt_client.crt","/run/secrets/mqtt_client.key",cert_reqs=ssl.CERT_REQUIRED,tls_version=ssl.PROTOCOL_TLSv1_2)
        while True:
            try:
                self._mqtt.connect(mqtthost,port=8883)
                break
            except:
                print("Waiting for mqtt...", flush=True)
                time.sleep(5)
        print("mqtt connected", flush=True)
    
    def __init__(self, pipeline, version="2", stop=Event()):
        super(RunVA, self).__init__()
        
        self._mqtt_connect()
        self.topic = None

        self._pipeline = pipeline
        self._version = version
        self._db = DBIngest(host=dbhost, index="algorithms", office=office)
        self._stop=stop

    def results_cb(self, data):
        self._mqtt.publish(self.topic, payload=data)

    def stop(self):
        print("stopping", flush=True)
        self._stop.set()
        self._mqtt.disconnect()

    def loop(self, sensor, location, uri, algorithm, algorithmName, options={}, topic="analytics"):
        try:
            self.topic = topic
            VAServing.start({
                'model_dir': '/home/models',
                'pipeline_dir': '/home/pipelines',
                'max_running_pipelines': 1,
            })

            try:
                result_filename = "/tmp/results_{}.jsonl".format(algorithm)
                source={
                    "type": "uri",
                    "uri": uri,
                }
                destination={
                    "type":"file",
                    "path":result_filename,
                    "format":"json-lines"
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

                filewatch = FileWatcher(result_filename)
                filewatch.start(self)

                self._stop.clear()
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

                        try:
                            self._db.update(algorithm, {
                                "sensor": sensor,
                                "performance": status.avg_fps,
                                "latency": avg_pipeline_latency * 1000,
                                "cpu": psutil.cpu_percent(),
                                "memory": psutil.virtual_memory().percent,
                            })
                        except:
                            print("Failed to update algorithm status", flush=True)
                            self._stop.set()
                            raise

                    self._stop.wait(3)

                self._stop=None
                pipeline.stop()
                filewatch.stop()
            except:
                print(traceback.format_exc(), flush=True)

            VAServing.stop()
        except:
            print(traceback.format_exc(), flush=True)
