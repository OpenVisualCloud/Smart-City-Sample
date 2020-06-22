#!/usr/bin/python3

from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler
import requests
import os

office=list(map(float,os.environ["OFFICE"].split(",")))
sthost=os.environ["STHOST"]

class Handler(FileSystemEventHandler):
    def __init__(self, sensor):
        super(Handler,self).__init__()
        self._sensor = sensor
        self._last_file = None
    
    def on_created(self, event):
        print("on_created: "+event.src_path, flush=True)
        if event.is_directory: return
        if event.src_path.endswith(".png"): return
        if self._last_file:
            if self._last_file==event.src_path: return
            try:
                self._process_file(self._last_file)
            except Exception as e:
                print("Exception: "+str(e), flush=True)
        self._last_file = event.src_path

    def _process_file(self, filename):
        with open(filename,"rb") as fd:
            r=requests.post(sthost,data={
                "time":str(int(int(os.path.basename(filename).split('_')[-2])/1000000)),
                "office":str(office[0])+","+str(office[1]),
                "sensor":self._sensor,
            },files={
                "file": fd,
            },verify=False)
        os.remove(filename)

class Rec2DB(object):
    def __init__(self, sensor):
        super(Rec2DB,self).__init__()
        self._sensor=sensor
        self._observer=Observer()

    def start(self):
        folder="/tmp/rec/"+self._sensor
        os.makedirs(folder, exist_ok=True)

        handler=Handler(self._sensor)
        self._observer.schedule(handler, folder, recursive=True)
        self._observer.start()

    def stop(self):
        self._observer.stop()
        self._observer.join()
