#!/usr/bin/python3

from db_ingest import DBIngest
from db_query import DBQuery
from signal import signal, SIGTERM

from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler

from threading import Timer
from probe import probe, run
import os
import tempfile
import shutil
import re
import sys

if len(sys.argv)<2:
    print("Usage: <sensor>")
    exit(-1)

office=list(map(float,os.environ["OFFICE"].split(",")))
dbhost=os.environ["DBHOST"]
storage=os.environ["STORAGE_VOLUME"]

class Handler(FileSystemEventHandler):
    def __init__(self, sensor):
        super(Handler,self).__init__()
        self.sensor = sensor
        self.db_rec = DBIngest(host=dbhost, index="recordings", office=office)
        self.db_cam = DBQuery(host=dbhost, index="sensors", office=office)
        self.last_file = None
        self.timer = None
    
    def on_created(self, event):
        if event.is_directory: return
        if event.src_path.endswith(".png"): return
        if self.last_file and (self.last_file==event.src_path): return
        if self.last_file:
            try:
                self.ingest()
            except Exception as error:
                print("Failed to ingest: %s %s" %(self.last_file,error), flush=True)

        self.last_file = event.src_path

        if self.timer: 
            self.timer.cancel()
            del(self.timer)
        self.timer = Timer(80, self.ingest)
        self.timer.start()
                    
    def ffmpeg_convert(self,filename):        
        with tempfile.TemporaryDirectory() as tmpdirname:
            filename = os.path.abspath(filename)
            tmpfilename = os.path.abspath(os.path.join(tmpdirname,os.path.basename(filename)))
            output=""
            try:
                list(run(["/usr/bin/ffmpeg","-i",filename,"-c","copy",tmpfilename]))
                shutil.move(tmpfilename,filename)
                list(run(["/usr/bin/ffmpeg","-i",filename,"-vf","thumbnail,scale=640:360","-frames:v","1",filename+".png"]))
                return filename,probe(filename)
            except Exception as error:
                print("Error converting mp4 with ffmpeg: %s %s" %(error,error.output), flush=True)
                raise

    def get_timestamp(self,filename):
        parsed = os.path.basename(filename).split('_')
        return int(int(parsed[-2])/1000000)

    def ingest(self):
        converted_file,sinfo=self.ffmpeg_convert(self.last_file)
        sinfo.update({
            "sensor": self.sensor,
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

        self.db_cam.update(self.sensor, {"bandwidth": bandwidth})
        self.db_rec.ingest(sinfo)


observer=None
watch=None

def quit_service(signum, sigframe):
    if observer: 
        if watch: observer.unschedule(watch)
        observer.stop()
    
signal(SIGTERM, quit_service)
sensor=sys.argv[1]
observer=Observer()
observer.start()
folder=os.path.join(os.path.realpath(storage),sensor)
os.makedirs(folder, exist_ok=True)
handler=Handler(sensor=sensor)
watch=observer.schedule(handler, folder, recursive=True)
observer.join()
