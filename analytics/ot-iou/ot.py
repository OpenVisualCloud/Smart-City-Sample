#!/usr/bin/python3
import traceback
import paho.mqtt.client as mqtt
from threading import Thread, Condition, Timer
from signal import signal, SIGTERM
from configuration import env
import json
import time
import datetime
import sys
import struct
from iou_tracker import IOUTracker
from utils import BBUtil

mqtthost = env["MQTTHOST"]
office = list(map(float, env["OFFICE"].split(",")))
mqtt_topic = env["MQTT_TOPIC"]

class OT(object):
    def __init__(self):
        super(OT, self).__init__()
        self._cache_rec = []
        self._cache_send = []
        self._cond_rec = Condition()
        self._cond_send = Condition()
        self._last_ts = None
        self._speed_total=0
        self._nframes=0
        self._max_speed=0

        self._mqtt = mqtt.Client()
        self._mqtt.on_message = self.on_message
        self._mqtt.on_disconnect = self.on_disconnect
        self._topic_last_ts=0
        self._tracker={}

    def loop(self, topic=mqtt_topic):
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
        Thread(target=self.process).start()
        Thread(target=self.publish).start()

        self._mqtt.subscribe(topic)
        self._mqtt.loop_forever()

    def _connect_watchdog(self):
        print("quit due to mqtt timeout", flush=True)
        exit(-1)

    def _add_rec(self, item=None):
        self._cond_rec.acquire()
        if item:
            self._cache_rec.append(item)
        self._cond_rec.notify()
        self._cond_rec.release()

    def _add_send(self, item=None):
        self._cond_send.acquire()
        if item:
            self._cache_send.append(item)
        self._cond_send.notify()
        self._cond_send.release()

    def stop(self):
        self._mqtt.disconnect()

    def on_disconnect(self, client, userdata, rc):
        self._stop = True

    def on_message(self, client, userdata, message):
        try:
            topic = message.topic
            now=time.time()
            self._add_rec(message.payload)
            delta=int((now - self._topic_last_ts)*1000)
            #print("MQTT on message: " +topic, delta, int((time.time()-now)*1000), flush=True)
            self._topic_last_ts=now

        except:
            print(traceback.format_exc(), flush=True)

    def _tracking(self,payload):
        metadata = json.loads(payload.decode("utf-8"))

        sensor=metadata["tags"]["sensor"]
        if sensor not in self._tracker:
            self._tracker[sensor]=IOUTracker(sigma_l=0,sigma_h=0.5,sigma_iou=0.5,t_min=2)

        tracker=self._tracker[sensor]
        width = metadata["resolution"]["width"]
        height = metadata["resolution"]["height"]
        bbutil=BBUtil(width, height)

        objects=metadata["objects"]
        bboxs=[]
        confidence=[]
        object_type=[]
        detections=[]
        for _idx in range(len(objects)):
            bbox=objects[_idx]["detection"]["bounding_box"]
            bbox=[bbox["x_min"],bbox["y_min"],bbox["x_max"],bbox["y_max"]]
            bboxs=bbutil.float_to_int(bbox)
            detections += [{
                "bbox":bbox,
                "confidence": objects[_idx]["detection"]["confidence"],
                "object_type": objects[_idx]["detection"]["label_id"],
                "idx": _idx,
                }]

        results=[]
        t=time.time()
        results=tracker.track(detections)
        #print("mot: ",int((time.time()-t)*1000),sensor,flush=True)

        if len(results) == 0: return
        for item in results:
           objects[item["idx"]]["track_id"]=item["track_id"]
        metadata["objects"]=[objects[item["idx"]] for item in results]
        metadata["nobjects"]=len(results)
        self._add_send(metadata)

    def process(self):
        while not self._stop:
            self._cond_rec.acquire()
            self._cond_rec.wait()
            bulk = self._cache_rec
            self._cache_rec = []
            self._cond_rec.release()

            try:
                for idx,item in enumerate(bulk):
                    t=time.time()
                    self._tracking(item)
            except:
                print(traceback.format_exc(), flush=True)
                continue

    def publish(self):
        while not self._stop:
            self._cond_send.acquire()
            self._cond_send.wait()
            bulk = self._cache_send
            self._cache_send = []
            self._cond_send.release()
            topic="analytics"

            try:
                for idx in range(len(bulk)):
                    t=time.time()
                    data = json.dumps(bulk[idx])
                    self._mqtt.publish(topic,payload=data,qos=0)
                pass
            except:
                print(traceback.format_exc(), flush=True)
                continue

ot = OT()

def quit_service(signum, sigframe):
    ot.stop()


signal(SIGTERM, quit_service)
ot.loop()
