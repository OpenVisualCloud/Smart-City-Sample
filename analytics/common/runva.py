#!/usr/bin/python3

import os
from db_ingest import DBIngest
from vaserving.vaserving import VAServing
from vaserving.pipeline import Pipeline
import time

mqtthost = os.environ["MQTTHOST"]
dbhost = os.environ["DBHOST"]
every_nth_frame = int(os.environ["EVERY_NTH_FRAME"])
office = list(map(float, os.environ["OFFICE"].split(",")))


class RunVA(object):
    def __init__(self, pipeline, version="2"):
        super(RunVA, self).__init__()
        self._pipeline = pipeline
        self._version = version
        self._db = DBIngest(host=dbhost, index="algorithms", office=office)
        self._stop = None
        self._pause = 0.5

        vaserving_args = {'model_dir': '/home/models',
                          'pipeline_dir': '/home/pipelines',
                          'max_running_pipelines': 1,
                          'log_level': "INFO"}

        VAServing.start(vaserving_args)

    def stop(self):
        self._stop = True

    def loop(self, sensor, location, uri, algorithm, algorithmName,
             resolution={"width": 0, "height": 0}, zonemap=[], topic="analytics"):
        try:
            source = {"uri": uri, "type": "uri"}

            destination = {"type": "mqtt", "host": mqtthost,
                           "clientid": algorithm, "topic": topic}

            tags = {"sensor": sensor, "location": location, "algorithm": algorithm,
                    "office": {"lat": office[0], "lon": office[1]}}

            parameters = {"inference-interval": every_nth_frame,
                          "recording_prefix": "/tmp/" + sensor}

            if algorithmName == "crowd-counting":
                parameters.update({"crowd_count": {
                    "width": resolution["width"],
                    "height": resolution["height"],
                    "zonemap": zonemap}})

            pipeline = VAServing.pipeline(self._pipeline, self._version)
            instance_id = pipeline.start(source=source,
                                         destination=destination,
                                         tags=tags,
                                         parameters=parameters)

            if instance_id is None:
                print("Pipeline {} version {} Failed to Start".format(
                    self._pipeline, self._version), flush=True)
                return

            while not self._stop:

                status = pipeline.status()

                print(status, flush=True)

                if (status.state.stopped()):
                    print("Pipeline {} Version {} Instance {} Ended with {}".format(
                        self._pipeline, self._version, instance_id, status.state.name), flush=True)
                    break

                if status.avg_fps > 0 and status.state is Pipeline.State.RUNNING:
                    avg_pipeline_latency = status.avg_pipeline_latency
                    if not avg_pipeline_latency:
                        avg_pipeline_latency = 0

                    self._db.update(algorithm, {
                        "sensor": sensor,
                        "performance": status.avg_fps,
                        "latency": avg_pipeline_latency * 1000})

                time.sleep(self._pause)

            print("exiting va pipeline", flush=True)
            pipeline.stop()
            VAServing.stop()
        except Exception as error:
            print("EXIT VA LOOP:{}".format(error), flush=True)
