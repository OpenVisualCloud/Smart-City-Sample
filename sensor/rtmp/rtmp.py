#!/usr/bin/python3

from signal import SIGTERM, signal
from db_query import DBQuery
from probe import probe
from configuration import env
import traceback
import time
from nginx import NGINX

service_interval = float(env.get("SERVICE_INTERVAL","30"))
office = list(map(float,env["OFFICE"].split(","))) if "OFFICE" in env else None
dbhost= env.get("DBHOST",None)

nginx1=NGINX()

def quit_service(signum, sigframe):
    nginx1.stop()
    exit(143)

signal(SIGTERM, quit_service)

nginx1.start()

dbs=DBQuery(index="sensors",office=office,host=dbhost)

# compete for a sensor connection
while True:
    try:
        for sensor in dbs.search("type:'camera' and status:'disconnected' and office:["+str(office[0])+","+str(office[1])+"]"):
            try:
                if sensor["_source"]["url"].split(":")[0] != "rtmp": continue
                if "start_time" in sensor["_source"] and sensor["_source"]["start_time"] < 0: continue
                rtmpuri=sensor["_source"]["url"]
                sinfo=probe(rtmpuri)
                if sinfo["resolution"]["width"]!=0 and sinfo["resolution"]["height"]!=0:
                    print("RTMP status disconnected->idle:", sensor["_id"], sensor["_source"]["subtype"], flush=True)
                    # ready for connecting
                    sinfo.update({"status":"idle"})
                r=dbs.update(sensor["_id"],sinfo,seq_no=sensor["_seq_no"],primary_term=sensor["_primary_term"])
            except Exception as e:
                print("Exception: "+str(e), flush=True)
    except Exception as e:
        print("Exception: "+str(e), flush=True)
    time.sleep(service_interval)

