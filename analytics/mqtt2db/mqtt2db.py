#!/usr/bin/python3

from db_ingest import DBIngest
import paho.mqtt.client as mqtt
from threading import Thread, Condition, Timer
from signal import signal, SIGTERM
import traceback
import json
import time
import sys
import os

mqtthost = os.environ["MQTTHOST"]
scenario = os.environ["SCENARIO"]
dbhost = os.environ["DBHOST"]
office = list(map(float, os.environ["OFFICE"].split(",")))

class MQTT2DB(object):
    def __init__(self):
        super(MQTT2DB, self).__init__()

        self._db = DBIngest(host=dbhost, index="analytics", office=office)
        self._cache = []
        self._cond = Condition()

        self._mqtt = mqtt.Client()
        self._mqtt.on_message = self.on_message
        self._mqtt.on_disconnect = self.on_disconnect

    def loop(self, topic="analytics"):
        print("connecting mqtt", flush=True)
        timer = Timer(10, self._connect_watchdog)
        timer.start()
        while True:
            try:
                self._mqtt.connect(mqtthost)
                break
            except:
                print(traceback.format_exc(), flush=True)
        timer.cancel()
        print("mqtt connected", flush=True)

        self._stop = False
        Thread(target=self.todb).start()

        self._mqtt.subscribe(topic)
        self._mqtt.loop_forever()

    def _connect_watchdog(self):
        print("quit due to mqtt timeout", flush=True)
        exit(-1)

    def _add1(self, item=None):
        self._cond.acquire()
        if item:
            self._cache.append(item)
        self._cond.notify()
        self._cond.release()

    def stop(self):
        self._mqtt.disconnect()

    def on_disconnect(self, client, userdata, rc):
        self._stop = True
        self._add1()

    def on_message(self, client, userdata, message):
        try:

            r = json.loads(str(message.payload.decode("utf-8", "ignore")))

            if "tags" in r:
                r.update(r["tags"])
                del r["tags"]

            if ("time" not in r) and ("real_base" in r) and ("timestamp" in r): 
                real_base=r["real_base"] if "real_base" in r else 0
                r["time"] = int((real_base + r["timestamp"]) / 1000000)

            if "objects" in r and scenario == "traffic":
                r["nobjects"] = int(len(r["objects"]))
            if "objects" in r and scenario == "stadium":
                r["count"] = {"people": len(r["objects"])}
            if "count" in r:
                r["nobjects"] = int(max([r["count"][k] for k in r["count"]]))

        except:
            print(traceback.format_exc(), flush=True)

        self._add1(r)

    def todb(self):
        while not self._stop:
            self._cond.acquire()
            self._cond.wait()
            bulk = self._cache
            self._cache = []
            self._cond.release()

            try:
                self._db.ingest_bulk(bulk)
            except:
                print(traceback.format_exc(), flush=True)


mqtt2db = MQTT2DB()


def quit_service(signum, sigframe):
    mqtt2db.stop()


signal(SIGTERM, quit_service)
mqtt2db.loop()
