#!/usr/bin/python3

from db_ingest import DBIngest
from threading import Event
from vaserving.vaserving import VAServing
from vaserving.pipeline import Pipeline
from configuration import env
from filewatch import FileWatcher
from result2db import Result2DB
import time
import traceback
import psutil
import json
from object_tracker import OT

dbhost = env["DBHOST"]
every_nth_frame = int(env["EVERY_NTH_FRAME"])
office = list(map(float, env["OFFICE"].split(",")))

class RunVA(object):
    
    def __init__(self, pipeline, version="2", stop=Event()):
        super(RunVA, self).__init__()
        
        self._pipeline = pipeline
        self._version = version
        self._db = DBIngest(host=dbhost, index="algorithms", office=office)
        self._stop = stop
        self._mode = None
        self._ot = OT()
        self._result2db = Result2DB()

    def result_cb(self, data):
        try:
            metadata = json.loads(data)
            if(self._mode == "analytics"):
                self._result2db.add_analytics_result(metadata)
            elif(self._mode == "relayanalytics"):
                ret = self._ot.tracking(metadata)
                self._result2db.add_analytics_result(ret)
            else:
                print("error mode = " + self._mode)
        except:
            print(traceback.format_exc(), flush=True)

    def stop(self):
        print("stopping", flush=True)
        self._stop.set()

    def loop(self, sensor, location, uri, algorithm, algorithmName, options={}, mode="analytics"):
        try:
            
            self._mode = mode

            VAServing.start({
                'model_dir': '/home/models',
                'pipeline_dir': '/home/pipelines',
                'max_running_pipelines': 1,
            })
            
            result_filename = "/tmp/results_{}.jsonl".format(algorithm)
            filewatch = FileWatcher(result_filename)

            try:
                
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

                
                filewatch.start(self)
                self._result2db.start()

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
                
            except:
                print(traceback.format_exc(), flush=True)

            filewatch.stop()
            self._result2db.stop()
                
            VAServing.stop()
        except:
            print(traceback.format_exc(), flush=True)
