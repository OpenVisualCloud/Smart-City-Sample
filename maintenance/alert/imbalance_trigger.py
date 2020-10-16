#!/usr/bin/python3

from db_query import DBQuery
from trigger import Trigger
from language import text
from configuration import env

service_interval=list(map(float,env["SERVICE_INTERVAL"].split(",")))
office=list(map(float, env["OFFICE"].split(",")))
dbhost=env["DBHOST"]

class ImbalanceTrigger(Trigger):
    def __init__(self):
        super(ImbalanceTrigger,self).__init__()
        self._dbs=DBQuery(index="sensors",office=office,host=dbhost)
        self._dba=DBQuery(index="algorithms",office=office,host=dbhost)

    def trigger(self, stop):
        stop.wait(service_interval[2])
        info=[]

        try:
            nsensors={
                "total": self._dbs.count("type='camera'"),
                "streaming": self._dbs.count("type='camera' and status='streaming'"),
                "idle": self._dbs.count("type='camera' and status='idle'"),
            }
            nalgorithms={
                "total": self._dba.count("name:*"),
            }
        except Exception as e:
            print("Exception: "+str(e), flush=True)
            return info
   
        if nsensors["total"]>nsensors["streaming"]+nsensors["idle"]:
            info.append({
                "fatal": [{ 
                    "message": text["check sensor"].format(nsensors["total"]-nsensors["streaming"]-nsensors["idle"]),
                    "args": nsensors,
                }]
            })

        if nalgorithms["total"]>nsensors["streaming"]+nsensors["idle"]:
            info.append({
                "warning": [{
                    "message": text("imbalance").format(nalgorithms["total"],nsensors["streaming"]+nsensors["idle"]),
                    "args": {
                        "nalgorithms": nalgorithms["total"],
                        "nsensors": nsensors["streaming"]+nsensors["idle"],
                    },
                }],
            })

        return info
