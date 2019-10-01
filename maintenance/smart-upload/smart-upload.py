#!/usr/bin/python3

from db_ingest import DBIngest
from db_query import DBQuery
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

def download_file(r):
    local_filename = r.url.split('/')[-1]
    # # NOTE the stream=True parameter below
    # r.raise_for_status()
    # with open(local_filename, "wb") as f:
        # for chunk in r.iter_content(chunk_size=8192):
            # if chunk: # filter out keep-alive new chunks
                # f.write(chunk)
                # # f.flush()
    return local_filename

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
            filename=smhost+'/'+q["_source"]["path"]
            #print("update: ", filename)
            #print("time: ", (os.path.basename(filename).split('.')[0]) )
            #print("office: ", str(office[0])+","+str(office[1]))

            r=requests.get(filename, timeout=1)
            if r.status_code!=200: 
                print("pipeline status: "+str(r.status_code), flush=True)
                print(r.text, flush=True)
                break

            print("get url: ", r.url)
            local_filename = download_file(r)
            print("download to: ", local_filename)

            # #add updates to request
            # with open(filename,"rb") as fd:
                # r=requests.post(sthost,data={
                    # "time":str((os.path.basename(filename).split('.')[0])),
                    # "office":str(office[0])+","+str(office[1]),
            # },files={
                    # "file": fd,
                # },verify=False)
            # #os.remove(filename)

    except Exception as e:
        print("Exception: "+str(e), flush=True)