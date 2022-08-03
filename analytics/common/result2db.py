#!/usr/bin/python3
# save analytics result to db

from db_ingest import DBIngest
from threading import Thread, Condition, Timer
from signal import signal, SIGTERM
from configuration import env
import traceback
import json

scenario = env["SCENARIO"]
dbhost = env["DBHOST"]
office = list(map(float, env["OFFICE"].split(",")))

class Result2DB(object):
    def __init__(self):
        super(Result2DB, self).__init__()

        self._db = DBIngest(host=dbhost, index="analytics", office=office)
        self._cache = []
        self._cond = Condition()
        self._stop = True
        self._thread = Thread(target=self.todbLoop)

    def start(self):
        if not self._stop:
            return
        self._stop = False
        self._thread.start()

    def _add1(self, item=None):
        self._cond.acquire()
        if item:
            self._cache.append(item)
        self._cond.notify()
        self._cond.release()

    def stop(self):
        if not self._stop:
            self._stop = True
            self._add1()
            self._thread.join()

    def add_analytics_result(self, metedata):
        try:

            if "tags" in metedata:
                metedata.update(metedata["tags"])
                del metedata["tags"]

            if ("time" not in metedata) and ("real_base" in metedata) and ("timestamp" in metedata): 
                real_base=metedata["real_base"] if "real_base" in metedata else 0
                metedata["time"] = int((real_base + metedata["timestamp"]) / 1000000)

            if "objects" in metedata and scenario == "traffic":
                metedata["nobjects"] = int(len(metedata["objects"]))
            if "objects" in metedata and scenario == "stadium":
                metedata["count"] = {"people": len(metedata["objects"])}
            if "count" in metedata:
                metedata["nobjects"] = int(max([metedata["count"][k] for k in metedata["count"]]))

        except:
            print(traceback.format_exc(), flush=True)

        self._add1(metedata)

    def todbLoop(self):
        while not self._stop:
            self._cond.acquire()
            self._cond.wait()
            bulk = self._cache
            self._cache = []
            self._cond.release()

            try:
                self._db.ingest_bulk(bulk)
            except:
                print(traceback.format_exc(), flush=True)
