#!/usr/bin/python3

from tornado import web, gen
from tornado.concurrent import run_on_executor
from concurrent.futures import ThreadPoolExecutor
from urllib.parse import unquote_plus
from signal import signal, SIGTERM
from db_query import DBQuery
from db_ingest import DBIngest
from probe import probe, run
from language import text
import traceback
import hashlib
import datetime
import time
import base64
import psutil
import json
import os

dbhost=os.environ["DBHOST"]
local_office=True if "OFFICE" in os.environ else False
halt_rec_th=float(os.environ["HALT_REC"])
fatal_disk_th=float(os.environ["FATAL_DISK"])
warn_disk_th=float(os.environ["WARN_DISK"])

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
            if sinfo["bandwidth"]:
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
                db_rec=DBIngest(host=dbhost, index="recordings", office=office)
                db_rec.ingest(sinfo)
        else:
            # ingest recording cloud
            if sinfo:
                db_s=DBQuery(host=dbhost, index="sensors", office=sinfo["office"])
                sensor=list(db_s.search("_id='"+sinfo["sensor"]+"'",size=1))
                if sensor:
                    # remove status
                    sensor[0]["_source"].pop("status",None)
                    # denormalize address
                    sinfo["address"]=sensor[0]["_source"]["address"]

                    # calcualte hash code for the sensor
                    m=hashlib.md5()
                    m.update(json.dumps(sensor[0]["_source"],ensure_ascii=False).encode('utf-8'))
                    md5=m.hexdigest()

                    # locate the sensor record in cloud
                    db_sc=DBQuery(host=dbhost, index="sensors", office="")
                    sensor_c=list(db_sc.search("md5='"+md5+"'",size=1))
                    if not sensor_c:  # if not available, ingest a sensor record in cloud
                        sensor_c=[{ "_source": sensor[0]["_source"].copy() }]
                        sensor_c[0]["_source"]["md5"]=md5
                        db_sc=DBIngest(host=dbhost, index="sensors", office="")
                        print("Ingest sensor: {}".format(sensor_c[0]["_source"]), flush=True)
                        sensor_c[0]=db_sc.ingest(sensor_c[0]["_source"])

                    # replace cloud sensor id and ingest recording
                    sinfo["sensor"]=sensor_c[0]["_id"]

                    print("Ingest recording: {}".format(sinfo), flush=True)
                    db_rec=DBIngest(host=dbhost, index="recordings", office="")
                    db_rec.ingest(sinfo)

                    # copy local analytics to cloud
                    db_a=DBQuery(host=dbhost, index="analytics", office=sinfo["office"])
                    data=[]
                    for r in db_a.search('sensor="'+sensor[0]["_id"]+'" and office:['+str(office[0])+','+str(office[1])+'] and time>='+str(sinfo["time"])+' and time<='+str(sinfo["time"]+sinfo["duration"]*1000),size=10000):
                        r["_source"]["sensor"]=sinfo["sensor"]
                        data.append(r["_source"])
                    db_ac=DBIngest(host=dbhost, index="analytics", office="")
                    print("Ingest analytics: {}".format(len(data)), flush=True)
                    db_ac.ingest_bulk(data)
                        
    @gen.coroutine
    def post(self):
        office=list(map(float,self.get_body_argument('office').split(",")))
        sensor=self.get_body_argument('sensor')
        timestamp=int(self.get_body_argument('time'))
        path=self.get_body_argument('file.path')
        yield self._rec2db(office, sensor, timestamp, path)
        self.set_status(400, "Return 400 to remove this file")

