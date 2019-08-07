#!/usr/bin/python3

from db_ingest import DBIngest
from db_query import DBQuery
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
        self._last_file = None
    
    def on_created(self, event):
        print("on_created: "+event.src_path, flush=True)
        if event.is_directory: return
        if event.src_path.endswith(".png"): return
        if self._last_file:
            if self._last_file==event.src_path: return
            try:
                if psutil.cpu_percent()>=80: time.sleep(2)  # yield on busy
                self._process_file(self._last_file)
            except Exception as e:
                print("Exception: "+str(e), flush=True)
        self._last_file = event.src_path

    def _ffmpeg_convert(self,filename): 
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
                return None,None

    def _get_timestamp(self,filename):
        parsed = os.path.basename(filename).split('_')
        return int(int(parsed[-2])/1000000)

    def _process_file(self, filename):
        converted_file,sinfo=self._ffmpeg_convert(filename)
        if not converted_file: return
        sinfo.update({
            "sensor": self._sensor,
            "office": {
                "lat": office[0],
                "lon": office[1],
            },
            "time": self._get_timestamp(converted_file),
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
        self._observer=Observer()
        self._watcher=None

    def loop(self):
        self._observer.start()

        folder=os.path.join(os.path.realpath(storage),self._sensor)
        print("Observing "+folder, flush=True)
        os.makedirs(folder, exist_ok=True)
        self._watcher=self._observer.schedule(self._handler, folder, recursive=True)

        self._observer.join()

    def stop(self):
        if self._watcher: self._observer.unschedule(self._watcher)
        self._observer.stop()
