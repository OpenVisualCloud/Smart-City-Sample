#!/usr/bin/python3

from db_ingest import DBIngest
from db_query import DBQuery
from probe import run
from signal import signal, SIGTERM
from language import text
from threading import Event
import traceback
import requests
import os

query=os.environ["QUERY"]
service_interval=float(os.environ["SERVICE_INTERVAL"])  # in seconds
office=list(map(float, os.environ["OFFICE"].split(",")))
dbhost=os.environ["DBHOST"]
sthostl=os.environ["STHOSTL"]
sthostc=os.environ["STHOSTC"]

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

            url=sthostl+'/'+q["_source"]["path"]
            print("url: "+url, flush=True)

            mp4file="/tmp/"+str(os.path.basename(url))

            print("Transcoding...", flush=True)
            # Replace with any transcoding command
            list(run(["/usr/local/bin/ffmpeg","-f","mp4","-i",url,"-c","copy","-f","mp4","-y",mp4file]))

            print("Uploading: "+ sthostc, flush=True)
            sensor=q["_source"]["sensor"]
            timestamp=q["_source"]["time"]

            upload(sthostc, mp4file, office, sensor, timestamp)
            os.remove(mp4file)
    except:
        print(traceback.format_exc(), flush=True)

    print("Sleeping...")
    stop.wait(service_interval)

dbs.delete(rs["_id"])
