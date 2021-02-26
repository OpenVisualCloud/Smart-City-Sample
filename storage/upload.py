#!/usr/bin/python3

from tornado import web, gen
from tornado.concurrent import run_on_executor
from concurrent.futures import ThreadPoolExecutor
from urllib.parse import unquote
from signal import signal, SIGTERM
from db_query import DBQuery
from db_ingest import DBIngest
from probe import probe, run
from language import text
from configuration import env
import datetime
import time
import psutil
import os

dbhost=env["DBHOST"]
local_office=True if "OFFICE" in env else False
halt_rec_th=float(env["HALT_REC"])
fatal_disk_th=float(env["FATAL_DISK"])
warn_disk_th=float(env["WARN_DISK"])

class UploadHandler(web.RequestHandler):
    def __init__(self, app, request, **kwargs):
        super(UploadHandler, self).__init__(app, request, **kwargs)
        self.executor= ThreadPoolExecutor(8)
        self._storage = "/var/www/mp4"

    def check_origin(self, origin):
        return True

    @run_on_executor
    def _rec2db(self, office, sensor, timestamp, path):
        disk_usage=psutil.disk_usage(self._storage)[3]
        if disk_usage<halt_rec_th:
            dt=datetime.datetime.fromtimestamp(timestamp/1000)
            officestr=(str(office[0])+"c"+str(office[1])).replace("-","n").replace(".","d")
            mp4path=self._storage+"/"+officestr+"/"+sensor+"/"+str(dt.year)+"/"+str(dt.month)+"/"+str(dt.day)
            os.makedirs(mp4path,exist_ok=True)
            mp4file=mp4path+"/"+str(timestamp)+".mp4"

            # perform a straight copy to fix negative timestamp for chrome
            list(run(["/usr/local/bin/ffmpeg","-f","mp4","-i",path,"-c","copy",mp4file]))

            sinfo=probe(mp4file)
            sinfo.update({
                "sensor": sensor,
                "office": {
                    "lat": office[0],
                    "lon": office[1],
                },
                "time": timestamp,
                "path": mp4file[len(self._storage)+1:],
            })
        else:
            print("Disk full: recording halted", flush=True)
            sinfo=None

        if local_office:
            if sinfo:
                if "bandwidth" in sinfo:
                    db_cam=DBQuery(host=dbhost, index="sensors", office=office)
                    db_cam.update(sensor, {"bandwidth": sinfo["bandwidth"]})

            # check disk usage and send alert
            disk_usage=psutil.disk_usage(self._storage).percent
            if disk_usage>=warn_disk_th:
                level="fatal" if disk_usage>=fatal_disk_th else "warning"
                db_alt=DBIngest(host=dbhost, index="alerts", office=office)
                message=text["halt recording"].format(disk_usage) if disk_usage>=halt_rec_th else text["disk usage"].format(disk_usage)
                db_alt.ingest({
                    "time": int(time.time()*1000),
                    "office": {
                        "lat": office[0],
                        "lon": office[1],
                    },
                    "location": {
                        "lat": office[0],
                        "lon": office[1],
                    },
                    level: [{
                        "message": message,
                        "args": {
                            "disk": disk_usage,
                        }
                    }]
                })

        # ingest recording local
        if sinfo:
            print("Ingest recording: {}".format(sinfo), flush=True)
            office1=office if local_office else ""

            # denormalize sensor address to recordings
            dbs=DBQuery(host=dbhost, index="sensors", office=office1)
            r=list(dbs.search("_id='"+sinfo["sensor"]+"'",size=1))
            if r: sinfo["address"]=r[0]["_source"]["address"]

            db_rec=DBIngest(host=dbhost, index="recordings", office=office1)
            db_rec.ingest(sinfo)
                        
    @gen.coroutine
    def post(self):
        office=list(map(float,self.get_body_argument('office').split(",")))
        print("office = {}".format(office), flush=True)
        sensor=self.get_body_argument('sensor')
        print("sensor = {}".format(sensor), flush=True)
        timestamp=int(self.get_body_argument('time'))
        print("timestamp = {}".format(timestamp), flush=True)
        path=self.get_body_argument('file.path')
        print("file.path = {}".format(path), flush=True)
        yield self._rec2db(office, sensor, timestamp, path)
        self.set_status(400, "Return 400 to remove this file")

