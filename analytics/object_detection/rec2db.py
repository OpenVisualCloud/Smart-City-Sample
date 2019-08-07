#!/usr/bin/python3

from db_ingest import DBIngest
from db_query import DBQuery
from interval import IntervalTimer
from threading import Lock
from probe import probe, run
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler
import psutil
import os
import tempfile
import shutil
import re
import sys

office=list(map(float,os.environ["OFFICE"].split(",")))
dbhost=os.environ["DBHOST"]
storage="/home/video-analytics/app/server/recordings"

class Handler(FileSystemEventHandler):
    def __init__(self, sensor):
        super(Handler,self).__init__()
        self._sensor = sensor
        self._db_rec = DBIngest(host=dbhost, index="recordings", office=office)
        self._db_cam = DBQuery(host=dbhost, index="sensors", office=office)
        self._lock = Lock()
        self._files = []
        self._last_file = None
    
    def on_created(self, event):
        print("on_created: "+event.src_path, flush=True)
        if event.is_directory: return
        if event.src_path.endswith(".png"): return
        if self._last_file:
            if self._last_file==event.src_path: return
            self._lock.acquire()
            self._files.append(self._last_file)
            self._lock.release()
        self._last_file = event.src_path

    def ffmpeg_convert(self,filename): 
        print("post-processing "+filename, flush=True)
        with tempfile.TemporaryDirectory() as tmpdirname:
            filename = os.path.abspath(filename)
            tmpfilename = os.path.abspath(os.path.join(tmpdirname,os.path.basename(filename)))
            try:
                list(run(["/usr/bin/ffmpeg","-i",filename,"-c","copy",tmpfilename]))
                shutil.move(tmpfilename,filename)
                list(run(["/usr/bin/ffmpeg","-i",filename,"-vf","thumbnail,scale=640:360","-frames:v","1",filename+".png"]))
                return filename,probe(filename)
            except Exception as e:
                print("Exception: "+str(e), flush=True)
                raise

    def get_timestamp(self,filename):
        parsed = os.path.basename(filename).split('_')
        return int(int(parsed[-2])/1000000)

    def on_timer(self):
        print("rec2db on_timer", flush=True)
        self._lock.acquire()
        files=self._files
        self._files=[]
        self._lock.release()

        while files:
            # yield CPU if the system is too busy
            if psutil.cpu_percent()>60: time.sleep(5)

            converted_file,sinfo=self.ffmpeg_convert(files.pop())
            sinfo.update({
                "sensor": self._sensor,
                "office": {
                    "lat": office[0],
                    "lon": office[1],
                },
                "time": self.get_timestamp(converted_file),
                "path": os.path.abspath(converted_file).split(os.path.abspath(storage)+"/")[1],
            })
        
            # calculate total bandwidth
            bandwidth=0
            for stream1 in sinfo["streams"]:
                if "bit_rate" in stream1: 
                    bandwidth=bandwidth+stream1["bit_rate"]

            if bandwidth: self._db_cam.update(self._sensor, {"bandwidth": bandwidth})
            self._db_rec.ingest(sinfo)
            print(sinfo, flush=True)

class Rec2DB(object):
    def __init__(self, sensor):
        super(Rec2DB,self).__init__()
        self._sensor=sensor
        self._handler=Handler(sensor)
        self._timer = IntervalTimer(15, self._handler.on_timer)
        self._observer=Observer()
        self._watcher=None

    def loop(self):
        self._observer.start()
        self._timer.start()

        folder=os.path.join(os.path.realpath(storage),self._sensor)
        print("Observing "+folder, flush=True)
        os.makedirs(folder, exist_ok=True)
        self._watcher=self._observer.schedule(self._handler, folder, recursive=True)

        self._observer.join()
        self._timer.cancel()

    def stop(self):
        if self._watcher: self._observer.unschedule(self._watcher)
        self._observer.stop()
        self._timer.cancel()
