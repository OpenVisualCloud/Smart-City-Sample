#!/usr/bin/python3

from concurrent.futures import ThreadPoolExecutor
from threading import Thread
import subprocess
import time
from configuration import env
from db_query import DBQuery

office = list(map(float,env["OFFICE"].split(","))) if "OFFICE" in env else None
dbhost= env.get("DBHOST",None)

class Streamer(object):
    def __init__(self):
        super(Streamer, self).__init__()
        self._sensors={}
        Thread(target=self._watcher_thread).start()
        self._dbs=DBQuery(index="sensors",office=office,host=dbhost)

    def get(self, sensor):
        if sensor not in self._sensors: return (None,None)
        return (self._sensors[sensor]["rtspuri"], self._sensors[sensor]["rtmpuri"])

    def set(self, sensor, rtspuri, rtmpuri,simulation):
        if sensor in self._sensors and self._sensors[sensor]["status"] == "streaming": return self._sensors[sensor]["status"]
        p = self._spawn(rtspuri, rtmpuri,simulation)
        if p.poll() == None:
            self._sensors[sensor]={
                "rtspuri": rtspuri,
                "rtmpuri": rtmpuri,
                "status": "streaming",
                "process": p,
            }
            return self._sensors[sensor]["status"]
        return "disconnected"

    def _update(self, sensor, status="streaming"):
        sinfo={"status":status}
        self._dbs.update(sensor, sinfo)

    def _spawn(self, rtspuri, rtmpuri,simulation=False):
        cmd = ["ffmpeg", "-i",rtspuri,"-vcodec", "copy", "-an", "-f", "flv", rtmpuri]
        if simulation == True:
            cmd = ["ffmpeg", "-i",rtspuri,"-vcodec", "libx264", "-preset:v", "ultrafast", "-tune:v", "zerolatency", "-an", "-f", "flv", rtmpuri]
        print(cmd, flush=True)
        p = subprocess.Popen(cmd)
        return p

    def _watcher_thread(self):
        while True:
            for sensor1 in self._sensors:
                if self._sensors[sensor1]["process"].poll() != None:
                    self._sensors[sensor1]["status"]="disconnected"
                    self._update(sensor1, status="disconnected")

            time.sleep(30)

