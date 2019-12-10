#!/usr/bin/python3

from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler
import requests
import os
import logging

log = logging.getLogger("rec2db")
log.setLevel(logging.INFO)

office=list(map(float,os.environ["OFFICE"].split(",")))
sthost=os.environ["STHOST"]

class Handler(FileSystemEventHandler):
    def __init__(self, sensor):
        log.info("============rec2db Handler: __init__============")
        super(Handler,self).__init__()
        self._sensor = sensor
        self._last_file = None
    
    def on_created(self, event):
        log.info("============rec2db Handler:on_created============")
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
        log.info("============rec2db Handler:_process_file============")
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
        log.info("============rec2db:__init__============")
        super(Rec2DB,self).__init__()
        self._sensor=sensor
        self._handler=Handler(sensor)
        self._observer=Observer()
        self._watcher=None

    def loop(self):
        log.info("============rec2db:loop============")
        self._observer.start()

        folder="/tmp/"+self._sensor
        os.makedirs(folder, exist_ok=True)
        self._watcher=self._observer.schedule(self._handler, folder, recursive=True)
        self._observer.join()

    def stop(self):
        log.info("============rec2db:stop============")
        if self._watcher: self._observer.unschedule(self._watcher)
        self._observer.stop()
