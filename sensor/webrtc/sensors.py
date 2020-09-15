#!/usr/bin/python3

from tornado import web, gen
from tornado.concurrent import run_on_executor
from concurrent.futures import ThreadPoolExecutor
from threading import Thread
from urllib.parse import unquote
from db_query import DBQuery
from owtapi import OWTAPI
import time
import os

DBHOST=os.environ["DBHOST"]
OFFICE=list(map(float,os.environ["OFFICE"].split(",")))
STREAMING_LIMIT=int(os.environ["STREAMING_LIMIT"])
INACTIVE_TIME=float(os.environ["INACTIVE_TIME"])
webrtchost=os.environ["WEBRTC_HOST"]

class RoomWatcher(object):
    def __init__(self):
        super(RoomWatcher, self).__init__()
        self._sensors={}
        Thread(target=self._cleanup_thread).start()

    def get(self, sensor):
        if sensor not in self._sensors: return (None,None)
        return (self._sensors[sensor]["room"], self._sensors[sensor]["stream"])

    def set(self, sensor, room, stream):
        if sensor in self._sensors: return
        self._sensors[sensor]={
            "room": room,
            "stream": stream,
            "time": int(time.time()),
        }

    def _cleanup_thread(self):
        owt=OWTAPI()
        while True:
            todelete=[]
            for sensor1 in self._sensors:
                participants=owt.list_participants(self._sensors[sensor1]["room"])
                now=int(time.time())
                if participants>0:
                    self._sensors[sensor1]["time"]=now
                elif now-self._sensors[sensor1]["time"]>INACTIVE_TIME:
                    todelete.append(sensor1)

            for d1 in todelete:
                print("Remove stream {}".format(self._sensors[d1]["stream"]), flush=True)
                owt.delete_stream(self._sensors[d1]["room"],self._sensors[d1]["stream"])
                print("Remove room {}".format(self._sensors[d1]["room"]), flush=True)
                owt.delete_room(self._sensors[d1]["room"])
                print("Remove sensor {}".format(d1), flush=True)
                self._sensors.pop(d1,None)

            time.sleep(30)
                    
watcher=RoomWatcher()

class SensorsHandler(web.RequestHandler):
    def __init__(self, app, request, **kwargs):
        super(SensorsHandler, self).__init__(app, request, **kwargs)
        self.executor=ThreadPoolExecutor(4)
        self._db=DBQuery(index="sensors", office=OFFICE, host=DBHOST)
        self._owt=OWTAPI()

    def check_origin(self, origin):
        return True

    def _room_details(self, sensor, room, stream):
        return {
            "sensor": sensor,
            "room": room,
            "stream": stream,
            "url": "{}?roomid={}&streamid={}".format(webrtchost,room,stream),
        }

    @run_on_executor
    def _create_room(self, sensor):
        r=list(self._db.search("_id='{}' and status='streaming'".format(sensor),size=1))
        if not r: return (404, "Sensor Not Found")

        room,stream=watcher.get(sensor)
        if room and stream:
            return self._room_details(sensor, room, stream)

        #rooms=self._owt.list_room()
        #room=rooms[0] if rooms else None
        room=self._owt.create_room(name=sensor,p_limit=STREAMING_LIMIT)

        rtsp_url=r[0]["_source"]["url"]
        stream=self._owt.start_streaming_ins(room=room,rtsp_url=rtsp_url) if room else None
        if not stream: return (503, "Exception when post")

        watcher.set(sensor, room, stream)
        return self._room_details(sensor, room, stream)

    @gen.coroutine
    def post(self):
        sensor=unquote(self.get_argument("sensor"))

        r=yield self._create_room(sensor)
        if isinstance(r, dict):
            self.write(r)
        else:
            self.set_status(r[0],r[1])

