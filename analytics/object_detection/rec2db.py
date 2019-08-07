#!/usr/bin/python3

from db_ingest import DBIngest
from db_query import DBQuery
from interval import IntervalTimer
from threading import Lock
from probe import probe, run
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler
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
        self._files = []
        self._lock = Lock()
        self._timer = IntervalTimer(10, self.on_timer)
        self._last_file = None
    
    def stop(self):
        self._timer.cancel()

    def on_created(self, event):
        if event.is_directory: return
        if event.src_path.endswith(".png"): return
        if self._last_file and (self._last_file==event.src_path): return
        if self._last_file:
            self._lock.acquire()
            self._files.append(self._last_file)
            self._lock.release()
        self._last_file = event.src_path

    def ffmpeg_convert(self,filename): 
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
        self._lock.acquire()
        file1=self._files.pop() if self._files else None
        self._lock.release()

        if not file1: return
        converted_file,sinfo=self.ffmpeg_convert(file1)
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

class Rec2DB(object):
    def __init__(self, sensor):
        super(Rec2DB,self).__init__()
        self._sensor=sensor
        self._handler=Handler(sensor)
        self._observer=None
        self._watcher=None

    def loop(self):
        self._observer=Observer()
        self._observer.start()

        folder=os.path.join(os.path.realpath(storage),sensor)
        os.makedirs(folder, exist_ok=True)
        self._watcher=self._observer.schedule(self._handler, folder, recursive=True)

        observer.join()
        self._handler.stop()

    def stop(self):
        if self._observer: 
            if self._watcher: self._observer.unschedule(self._watcher)
            self._observer.stop()
