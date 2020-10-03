#!/usr/bin/python3

from threading import Thread, Event
from owtapi import OWTAPI
from configuration import env
import time

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
        return (self._rooms[name]["room"], self._rooms[name]["stream"])

    def set(self, name, room, stream=None):
        if name in self._rooms: return
        self._rooms[name]={
            "room": room,
            "stream": stream,
            "time": int(time.time()),
        }

    def _cleanup_thread(self):
        owt=OWTAPI()
        while not self._stop.is_set():
            todelete=[]
            for name in self._rooms:
                try:
                    participants=owt.list_participants(self._rooms[name]["room"])
                except:
                    participants=0
                now=int(time.time())
                print("Watcher: room {} participant {} inactive {}".format(name,participants,now-self._rooms[name]["time"]), flush=True)
                if participants>0:
                    self._rooms[name]["time"]=now
                elif now-self._rooms[name]["time"]>self._inactive:
                    todelete.append(name)

            for name in todelete:
                stream1=self._rooms[name]["stream"]
                room1=self._rooms[name]["room"]

                try:
                    streams=[stream1] if stream1 else owt.list_streams(name)
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
