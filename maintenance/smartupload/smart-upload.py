#!/usr/bin/python3

from db_ingest import DBIngest
from db_query import DBQuery
from signal import signal, SIGTERM
import os
import time

print("enter smart-upload.py")
indexes=os.environ["INDEXES"].split(",")
service_interval=float(os.environ["SERVICE_INTERVAL"])  # in seconds
update_interval=float(os.environ["UPDATE_INTERVAL"])  # in seconds
search_batch=int(os.environ["SEARCH_BATCH"])
update_batch=int(os.environ["UPDATE_BATCH"])
office=list(map(float, os.environ["OFFICE"].split(",")))
dbhost=os.environ["DBHOST"]

while True:
    print("Sleeping...")
    time.sleep(service_interval)

    print("Searching...",flush=True)

