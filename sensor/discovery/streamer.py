#!/usr/bin/python3

from concurrent.futures import ThreadPoolExecutor
from threading import Thread
import subprocess
import time

class Streamer(object):
    def __init__(self):
        super(Streamer, self).__init__()
        self._sensors={}
        Thread(target=self._watcher_thread).start()

    def get(self, sensor):
        if sensor not in self._sensors: return (None,None)
        return (self._sensors[sensor]["rtspuri"], self._sensors[sensor]["rtmpuri"])

    def set(self, sensor, rtspuri, rtmpuri,simulation):
        if sensor in self._sensors: return
        p = self._spawn(rtspuri, rtmpuri,simulation)
        self._sensors[sensor]={
            "rtspuri": rtspuri,
            "rtmpuri": rtmpuri,
            "process": p,
        }

    def _spawn(self, rtspuri, rtmpuri,simulation=False):
        cmd = ["ffmpeg", "-i",rtspuri,"-vcodec", "copy", "-an", "-f", "flv", rtmpuri]
        if simulation == True:
            cmd = ["ffmpeg", "-i",rtspuri,"-vcodec", "libx264", "-preset:v", "ultrafast", "-tune:v", "zerolatency", "-an", "-f", "flv", rtmpuri]
        print(cmd, flush=True)
        p = subprocess.Popen(cmd)
        return p

    def _watcher_thread(self):
        while True:
            tospawn=[]
            for sensor1 in self._sensors:
                if self._sensors[sensor1]["process"].poll() != None:
                    tospawn.append(sensor1)

            for d1 in tospawn:
                print("Spawn sensor {} as thread exit".format(d1), flush=True)
                self._sensors[d1]["process"] = self._spawn(self._sensors[d1]["rtspuri"], self._sensors[d1]["rtmpuri"])
                
            time.sleep(30)

