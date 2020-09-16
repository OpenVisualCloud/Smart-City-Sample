#!/usr/bin/python3

from db_ingest import DBIngest
from db_query import DBQuery
from probe import run
from signal import signal, SIGTERM
from language import text
from threading import Event
from configuration import env
import traceback
import requests
import hashlib
import json
import os

query=env["QUERY"]
service_interval=float(env["SERVICE_INTERVAL"])  # in seconds
office=list(map(float, env["OFFICE"].split(",")))
dbhost=env["DBHOST"]
sthostl=env["STHOSTL"]
dbchost=env["DBCHOST"]
sthostc=env["STHOSTC"]

stop=Event()
def quit_service(signum, sigframe):
    stop.set()

def upload(cloudhost, filename, office, sensor, timestamp):
    with open(filename,"rb") as fd:
        r=requests.post(cloudhost,data={
            "time":timestamp,
            "office":str(office[0])+","+str(office[1]),
            "sensor":sensor,
        },files={
            "file": fd,
        },verify=False)

signal(SIGTERM, quit_service)
dbs=DBIngest(index="services",office=office,host=dbhost)
dbs.wait(stop)
rs=dbs.ingest({
    "name": text["smart-upload"],
    "service": text["maintanence"],
    "status": "active",
})

dbq=DBQuery(index="recordings",office=office,host=dbhost)
dbs=DBQuery(index="sensors",office=office,host=dbhost)
dba=DBQuery(index="analytics",office=office,host=dbhost)

dbsq_c=DBQuery(index="sensors",office="",host=dbchost)
dbsi_c=DBIngest(index="sensors",office="",host=dbchost)
dba_c=DBIngest(index="analytics",office="",host=dbchost)

while not stop.is_set():
    print("Searching...",flush=True)
    try:
        for q in dbq.search("not evaluated=true", size=25):
            if stop.is_set(): break

            # mark it as evaluated
            dbq.update(q["_id"],{ "evaluated": True })

            # make the upload decision based on analytics queries
            r=list(dba.search("( " + query + " ) and ( sensor='"+q["_source"]["sensor"]+"' and time>"+str(q["_source"]["time"])+" and time<"+ str(q["_source"]["time"]+q["_source"]["duration"]*1000) +" ) ", size=1))
            if not r: 
                stop.wait(2)
                continue

            # get the sensor record
            sensor=list(dbs.search("_id='"+q["_source"]["sensor"]+"'",size=1))
            if not sensor: raise Exception("Sensor not found")

            # remove status
            sensor[0]["_source"].pop("status",None)

            # calcualte hash code for the sensor
            m=hashlib.md5()
            m.update(json.dumps(sensor[0]["_source"],ensure_ascii=False).encode('utf-8'))
            md5=m.hexdigest()

            # locate the sensor record in cloud
            sensor_c=list(dbsq_c.search("md5='"+md5+"'",size=1))
            if not sensor_c:  # if not available, ingest a sensor record in cloud
                sensor_c=[{ "_source": sensor[0]["_source"].copy() }]
                sensor_c[0]["_source"]["md5"]=md5

                sensor_c[0]=dbsi_c.ingest(sensor_c[0]["_source"])
                print("Ingest sensor: {}".format(sensor_c[0]["_id"]), flush=True)

            analytics=[]
            for r in dba.search("sensor='"+q["_source"]["sensor"]+"' and time>"+str(q["_source"]["time"])+" and time<"+ str(q["_source"]["time"]+q["_source"]["duration"]*1000),size=10000):
                r["_source"]["sensor"]=sensor_c[0]["_id"]
                analytics.append(r["_source"])

            print("Ingest analytics: {}".format(len(analytics)), flush=True)
            dba_c.ingest_bulk(analytics)

            url=sthostl+'/'+q["_source"]["path"]
            print("url: "+url, flush=True)

            mp4file="/tmp/"+str(os.path.basename(url))

            print("Transcoding...", flush=True)
            # Replace with any transcoding command
            list(run(["/usr/local/bin/ffmpeg","-f","mp4","-i",url,"-c","copy","-f","mp4","-y",mp4file]))

            print("Uploading: "+ sthostc, flush=True)
            sensor=sensor_c[0]["_id"]
            timestamp=q["_source"]["time"]

            upload(sthostc, mp4file, office, sensor, timestamp)
            os.remove(mp4file)
    except:
        print(traceback.format_exc(), flush=True)

    print("Sleeping...")
    stop.wait(service_interval)

dbs.delete(rs["_id"])
