#!/usr/bin/python3

from db_ingest import DBIngest
from signal import signal, SIGTERM
import paho.mqtt.client as mqtt
from threading import Timer, Lock
import json
import time
import sys
import os

if len(sys.argv)<3:
    print("Usage: <algorithm> <topic>")
    exit(-1)

mqtthost = os.environ["MQTTHOST"]
dbhost = os.environ["DBHOST"]
office = list(map(float, os.environ["OFFICE"].split(",")))

class IntervalTimer(Timer):
    def run(self):
        while not self.finished.wait(self.interval):
            self.function(*self.args, **self.kwargs)

class MQTT2DB(object):
    def __init__(self, algorithm):
        super(MQTT2DB,self).__init__()
        self._mqtt=mqtt.Client("feeder_" + algorithm)
        self._db=DBIngest(host=dbhost, index="analytics", office=office)
        self._cache=[]
        self._lock=Lock()
        self._timer=IntervalTimer(2.0, self.on_timer)

    def loop(self, topic):
        while True:
            try:
                self._mqtt.connect(mqtthost)
                break
            except Exception as e:
                print("Exception: "+str(e), flush=True)
                time.sleep(10)

        self._mqtt.on_message = self.on_message
        self._mqtt.subscribe(topic)

        self._timer.start()
        self._mqtt.loop_forever()

    def stop(self):
        self._timer.cancel()
        self._mqtt.disconnect()

    def on_message(self, client, userdata, message):
        r=json.loads(str(message.payload.decode("utf-8", "ignore")))
        r.update(r["tags"])
        del r["tags"]
        r["time"]=int((r["real_base"]+r["timestamp"])/1000000)
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
            time.sleep(0.1)

mqtt2db=None

def quit_service(signum, sigframe):
    if mqtt2db: mqtt2db.stop()

signal(SIGTERM, quit_service)
mqtt2db=MQTT2DB(sys.argv[1])  # algorithm
mqtt2db.loop(sys.argv[2]) # topic
