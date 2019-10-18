#!/usr/bin/python3

from db_ingest import DBIngest
from signal import signal, SIGTERM
import paho.mqtt.client as mqtt
from threading import Lock, Timer
import json
import time
import sys
import os

mqtthost = os.environ["MQTTHOST"]
dbhost = os.environ["DBHOST"]
office = list(map(float, os.environ["OFFICE"].split(",")))

class IntervalTimer(Timer):
    def run(self):
        while not self.finished.is_set():
            self.finished.wait(self.interval)
            self.function(*self.args, **self.kwargs)
        self.finished.set()

class MQTT2DB(object):
    def __init__(self, algorithm):
        super(MQTT2DB,self).__init__()
        self._mqtt=mqtt.Client("feeder_" + algorithm)

        while True:
            try:
                self._mqtt.connect(mqtthost)
                break
            except Exception as e:
                print("Exception: "+str(e), flush=True)
                time.sleep(10)

        self._db=DBIngest(host=dbhost, index="analytics", office=office)
        self._cache=[]
        self._lock=Lock()
        self._timer=IntervalTimer(2.0, self.on_timer)

    def loop(self, topic):
        self._mqtt.on_message = self.on_message
        self._mqtt.subscribe(topic)
        self._timer.start()
        self._mqtt.loop_forever()

    def stop(self):
        self._timer.cancel()
        self._mqtt.disconnect()

    def on_message(self, client, userdata, message):
        try:
            r=json.loads(str(message.payload.decode("utf-8", "ignore")))
            r.update(r["tags"])
            del r["tags"]
            if "real_base" not in r: r["real_base"]=0
            r["time"]=int((r["real_base"]+r["timestamp"])/1000000)
            if "objects" in r: r["nobjects"]=int(len(r["objects"]))
        except Exception as e:
            print("Exception: "+str(e), flush=True)
        self._lock.acquire()
        self._cache.append(r)
        self._lock.release()

    def on_timer(self):
        self._lock.acquire()
        bulk=self._cache
        self._cache=[]
        self._lock.release()

        bulk_size=500
        while len(bulk):
            try: 
                self._db.ingest_bulk(bulk[:bulk_size])
                bulk=bulk[bulk_size:]
            except Exception as e:
                print("Exception: "+str(e), flush=True)
            time.sleep(0.25)
