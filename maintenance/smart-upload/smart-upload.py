#!/usr/bin/python3

from db_ingest import DBIngest
from db_query import DBQuery
from probe import probe, run
from signal import signal, SIGTERM
from language import text
import traceback
import requests
import os
import time

query=os.environ["QUERY"]
service_interval=float(os.environ["SERVICE_INTERVAL"])  # in seconds
office=list(map(float, os.environ["OFFICE"].split(",")))
dbhost=os.environ["DBHOST"]
smhost=os.environ["SMHOST"]
cloudhost=os.environ["CLOUDHOST"]

dbs=None
rs=None

def quit_service(signum, sigframe):
    if dbs and rs: dbs.delete(rs["_id"])
    exit(143)

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
while True:
    try:
        dbs.ingest({
            "name": text["smart-upload"],
            "service": text["maintanence"],
            "status": "active",
        })
        break
    except Exception as e:
        print("Waiting for DB...", flush=True)
        time.sleep(10)

dbq=DBQuery(index="recordings,analytics",office=office,host=dbhost)

while True:

    print("Searching...",flush=True)
    print("query = ", query)

    try:
        for q in dbq.search(query, size=25):
            # mark it as uploaded
            dbq.update(q["_id"],{ "uploaded": True })

            url=smhost+'/'+q["_source"]["path"]
            print("url: "+url, flush=True)

            mp4file="/tmp/"+str(os.path.basename(url))

            print("Transcoding...", flush=True)
            #list(run(["/usr/local/bin/ffmpeg","-f","mp4","-i",url,"-c:v","libsvt_hevc","-preset","9","-c:a","aac","-f","mp4","-y",mp4file]))
            list(run(["/usr/local/bin/ffmpeg","-f","mp4","-i",url,"-c","copy","-f","mp4","-y",mp4file]))

            print("Uploading: "+ cloudhost, flush=True)
            sensor=q["_source"]["sensor"]
            timestamp=q["_source"]["time"]
            upload(cloudhost, mp4file, office, sensor, timestamp)
            os.remove(mp4file)
    except:
        print(traceback.format_exc(), flush=True)

    print("Sleeping...")
    time.sleep(service_interval)
