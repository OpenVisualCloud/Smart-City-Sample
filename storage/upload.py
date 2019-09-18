#!/usr/bin/python3

from tornado import web, gen
from tornado.concurrent import run_on_executor
from concurrent.futures import ThreadPoolExecutor
from urllib.parse import unquote_plus
from signal import signal, SIGTERM
from db_query import DBQuery
from db_ingest import DBIngest
from probe import probe, run
import datetime
import base64
import os

dbhost=os.environ["DBHOST"]
recording_index=os.environ["RECORDING_INDEX"]
sensor_index=os.environ["SENSOR_INDEX"] if "SENSOR_INDEX" in os.environ else None

class UploadHandler(web.RequestHandler):
    def __init__(self, app, request, **kwargs):
        super(UploadHandler, self).__init__(app, request, **kwargs)
        self.executor= ThreadPoolExecutor(8)
        self._storage = "/var/www/mp4"

    def check_origin(self, origin):
        return True

    @run_on_executor
    def _rec2db(self, office, sensor, timestamp, path):
        dt=datetime.datetime.fromtimestamp(timestamp/1000)
        officestr=(str(office[0])+"c"+str(office[1])).replace("-","n").replace(".","d")
        mp4path=self._storage+"/"+officestr+"/"+sensor+"/"+str(dt.year)+"/"+str(dt.month)+"/"+str(dt.day)
        os.makedirs(mp4path,exist_ok=True)
        mp4file=mp4path+"/"+str(timestamp)+".mp4"

        list(run(["/usr/bin/ffmpeg","-f","mp4","-i",path,"-c","copy",mp4file]))
        list(run(["/usr/bin/ffmpeg","-i",mp4file,"-vf","scale=640:360","-frames:v","1",mp4file+".png"]))
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

        # calculate total bandwidth
        if sensor_index:
            bandwidth=0
            for stream1 in sinfo["streams"]:
                if "bit_rate" in stream1:
                    bandwidth=bandwidth+stream1["bit_rate"]
            if bandwidth: 
                db_cam=DBQuery(host=dbhost, index=sensor_index, office=office)
                db_cam.update(sensor, {"bandwidth": bandwidth})

        # ingest recording
        db_rec=DBIngest(host=dbhost, index=recording_index, office=office)
        db_rec.ingest(sinfo)

    @gen.coroutine
    def post(self):
        office=list(map(float,self.get_body_argument('office').split(",")))
        sensor=self.get_body_argument('sensor')
        timestamp=int(self.get_body_argument('time'))
        path=self.get_body_argument('file.path')
        yield self._rec2db(office, sensor, timestamp, path)
        self.set_status(400, "Return 400 to remove this file")
