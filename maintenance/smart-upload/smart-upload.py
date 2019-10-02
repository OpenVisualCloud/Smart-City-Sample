#!/usr/bin/python3

from db_ingest import DBIngest
from db_query import DBQuery
from probe import probe, run
from signal import signal, SIGTERM
import requests
import os
import time

query=os.environ["QUERY"]
indexes=os.environ["INDEXES"]
service_interval=float(os.environ["SERVICE_INTERVAL"])  # in seconds
update_interval=float(os.environ["UPDATE_INTERVAL"])  # in seconds
search_batch=int(os.environ["SEARCH_BATCH"])
update_batch=int(os.environ["UPDATE_BATCH"])
office=list(map(float, os.environ["OFFICE"].split(",")))
dbhost=os.environ["DBHOST"]
smhost=os.environ["SMHOST"]
cloudhost=os.environ["CLOUDHOST"]

def upload(cloudhost, filename, office, timestamp):
    print("time: "+timestamp)
    print("office: "+str(office[0])+","+str(office[1]))
    #print("sensor: "+sensor)
    with open(filename,"rb") as fd:
        r=requests.post(cloudhost,data={
            "time":timestamp,
            "office":str(office[0])+","+str(office[1]),
            #"sensor":#sensor,
        },files={
            "file": fd,
        },verify=False)
    os.remove(filename)
        
def quit_service(signum, sigframe):
    if dbs and rs: dbs.delete(rs["_id"])
    exit(143)

signal(SIGTERM, quit_service)
dbs=DBIngest(index="services",office=office,host=dbhost)
while True:
    try:
        dbs.ingest({
            "name": "smart-upload",
            "service": "maintanence",
            "status": "active",
        })
        break
    except Exception as e:
        print("Exception: "+str(e), flush=True)
        time.sleep(10)

dbq=DBQuery(index=indexes,office=office,host=dbhost)

while True:
    print("Sleeping...")
    time.sleep(service_interval)

    print("Searching...",flush=True)
    print("query = ", query)

    try:
        for q in dbq.search(query):
            url=smhost+'/'+q["_source"]["path"]
            print("url: ", url)

            mp4file="/tmp/"+str(os.path.basename(url))
            timestamp=(mp4file).split('.')[0]
            print("mp4file: ", mp4file)

            print("start ffmpeg transcoding")
            list(run(["/usr/bin/ffmpeg","-f","mp4","-i",url,"-c:v","libsvt_hevc",mp4file]))
            print("done ffmpeg transcoding")

            print("send to cloud storage: ", cloudhost)
            upload(cloudhost, mp4file, office, timestamp)
            print("done upload")


    except Exception as e:
        print("Exception: "+str(e), flush=True)
