#!/usr/bin/python3

from db_ingest import DBIngest
import time
import os

office=list(map(float, os.environ["OFFICE"].split(",")))
dbhost=os.environ["DBHOST"]

class Trigger(object):
    def __init__(self):
        super(Trigger,self).__init__()
        self.__db=DBIngest(index="alerts",office=office,host=dbhost)

    def trigger(self):
        return None

    def loop(self):
        while True:
            info=self.trigger()
            if not info: continue

            for v in info:
                v.update({
                    "time": int(time.time()*1000),
                    "office": {
                        "lat": office[0],
                        "lon": office[1],
                    },
                })
                if "location" not in v:
                    v["location"]=v["office"]

            self.__db.ingest_bulk(info)
