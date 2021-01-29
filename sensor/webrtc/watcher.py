#!/usr/bin/python3

from threading import Thread, Event
from owtapi import OWTAPI
from db_query import DBQuery
from configuration import env
import time

office = list(map(float,env["OFFICE"].split(","))) if "OFFICE" in env else None
dbhost= env.get("DBHOST",None)
inactive_time=float(env["INACTIVE_TIME"])

class RoomWatcher(object):
    def __init__(self, inactive=inactive_time, stop=Event()):
        super(RoomWatcher, self).__init__()
        self._stop=stop
        self._inactive=inactive
        self._rooms={}
        Thread(target=self._cleanup_thread).start()

    def get(self, name):
        if name not in self._rooms: return (None,None)
        return (self._rooms[name]["room"], self._rooms[name]["stream_in"])

    def _parse_name(self, name):
        items=name.split(":")
        return {"id": items[3], "type": items[1], "subtype": items[2]}

    def set(self, name, room, stream=None):
        if name in self._rooms: return
        self._rooms[name]={
            "room": room,
            "stream_in": stream,
            "stream_out": {
                "stream": None,
                "status": "idle",
                "rtmpurl": None,
            },
            "sensor": self._parse_name(name),
            "time": int(time.time()),
        }

    def set_stream_out(self, name, status, rtmpurl):
        if name not in self._rooms: return
        self._rooms[name]["stream_out"]= {"status": status, "rtmpurl": rtmpurl}

    def _cleanup_thread(self):
        owt=OWTAPI()
        dbs=DBQuery(index="sensors",office=office,host=dbhost)
        while not self._stop.is_set():
            todelete=[]
            tostartstreamout=[]
            tostopstreamout=[]
            for name in self._rooms:
                try:
                    participants=owt.list_participants(self._rooms[name]["room"])
                except:
                    participants=0
                now=int(time.time())
                print("Watcher: room {} participant {} inactive {} stream-out status {}".format(name,participants,now-self._rooms[name]["time"],self._rooms[name]["stream_out"]["status"]), flush=True)
                print(self._rooms[name], flush=True)
                if participants>0:
                    self._rooms[name]["time"]=now
                elif now-self._rooms[name]["time"]>self._inactive:
                    todelete.append(name)

                if self._rooms[name]["stream_out"]["status"] == "start":
                    tostartstreamout.append(name)
                elif self._rooms[name]["stream_out"]["status"] == "stop":
                    tostopstreamout.append(name)

            for name in tostartstreamout:
                if self._rooms[name]["sensor"]["subtype"] != "mobile_camera": continue
                sensor=self._rooms[name]["sensor"]
                stream1=self._rooms[name]["stream_in"]
                room1=self._rooms[name]["room"]
                rtmpurl=self._rooms[name]["stream_out"]["rtmpurl"]
                try:
                    stream1=stream1 if stream1 else owt.list_streams(room1)[0]
                except:
                    continue

                self._rooms[name]["stream_in"]=stream1
                if stream1 and rtmpurl:
                    try:
                        self._rooms[name]["stream_out"]["stream"] = owt.start_streaming_outs(room=room1,url=rtmpurl,video_from=stream1)["id"]
                    except:
                        continue
                else: continue

                try:
                    dbs.update(sensor["id"],{"status":"disconnected", "url":rtmpurl})
                except:
                    continue
                self._rooms[name]["stream_out"]["status"] = "streaming"

            for name in tostopstreamout:
                if self._rooms[name]["sensor"]["subtype"] != "mobile_camera": continue
                stream1=self._rooms[name]["stream_out"]["stream"]
                room1=self._rooms[name]["room"]
                if stream1:
                    try:
                        owt.stop_streaming_outs(room1,stream1)
                    except:
                        continue
                self._rooms[name]["stream_out"]["status"] = "idle"

            for name in todelete:
                stream1=self._rooms[name]["stream_in"]
                room1=self._rooms[name]["room"]

                try:
                    streams=[stream1] if stream1 else owt.list_streams(room1)
                except:
                    streams=[]

#                for stream1 in streams:
#                    print("Remove stream {}".format(stream1), flush=True)
#                    try:
#                        owt.delete_stream(room1,stream1)
#                    except:
#                        pass

                print("Remove room {}:{}".format(name,room1), flush=True)
                try:
                    owt.delete_room(room1)
                except:
                    pass

                self._rooms.pop(name,None)

            self._stop.wait(self._inactive/3.0)
