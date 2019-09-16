#!/usr/bin/python3

from db_ingest import DBIngest
import socket
import time
import os

dbhost=os.environ["DBHOST"]
office=list(map(float,os.environ["OFFICE"].split(",")))
host=os.environ["PROXYHOST"] if "PROXYHOST" in os.environ else "http://"+socket.gethostname()+":8080"

class Office(object):
    def __init__(self):
        super(Office,self).__init__()
        self._db=DBIngest(index="offices",office="",host=dbhost)
        self._r=None

    def reg(self):
        print("Register office: ["+str(office[0])+","+str(office[1])+"]",flush=True)
        while True:
            try:
                self._r=self._db.ingest({
                    "office": {
                        "lat": office[0],
                        "lon": office[1],
                    },
                    "uri": host,
                },"$".join(map(str,office)))
                break
            except Exception as e:
                print("Exception: "+str(e), flush=True)
                time.sleep(10)

    def unreg(self):
        print("Unregister office: ["+str(office[0])+","+str(office[1])+"]",flush=True)
        if self._r: self._db.delete(self._r["_id"])

