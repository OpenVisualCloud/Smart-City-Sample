#!/usr/bin/python3

from signal import SIGTERM, signal
from db_query import DBQuery
from db_ingest import DBIngest
from provision import Provision
import traceback
import requests
import time
import os
import json
import re

dbhost=os.environ["DBHOST"]
dbchost=os.environ["DBCHOST"]
office=list(map(float,os.environ["OFFICE"].split(",")))
replicas=list(map(int,os.environ["REPLICAS"].split(",")))

def quit_service():
    exit(143)

signal(SIGTERM, quit_service)

# wait until DB is ready
dbq=DBQuery(index="", office=office, host=dbhost)
while True:
    try:
        if dbq.health(): break
    except:
        print("Waiting for DB...", flush=True)
    time.sleep(1)
    
officestr=dbq.office()
settings={
    "offices": {
        "settings": {
            "index": {
                "number_of_shards": 1,
                "number_of_replicas": replicas[0],
            },
        },
        "mappings": {
            "properties": {
                "location": { "type": "geo_point", },
            },
        },
    },
    "provisions"+officestr: {
        "settings": {
            "index": {
                "number_of_shards": 1,
                "number_of_replicas": replicas[1],
            },
        },
        "mappings": {
            "properties": {
                "location": { "type": "geo_point", },
                "office": { "type": "geo_point", },
                "ip": { "type": "ip_range", },
            },
        },
    },
    "sensors"+officestr: {
        "settings": {
            "index": {
                "number_of_shards": 1,
                "number_of_replicas": replicas[1],
            },
        },
        "mappings": {
            "properties": {
                "office": { "type": "geo_point", },
                "location": { "type": "geo_point", },
                "ip": { "type": "ip_range", },
            },
        },
    },
    "sensors": {
        "settings": {
            "index": {
                "number_of_shards": 1,
                "number_of_replicas": replicas[0],
            },
        },
        "mappings": {
            "properties": {
                "office": { "type": "geo_point", },
                "location": { "type": "geo_point", },
                "ip": { "type": "ip_range", },
            },
        },
    },
    "recordings"+officestr: {
        "settings": {
            "index": {
                "number_of_shards": 1,
                "number_of_replicas": replicas[1],
            },
        },
        "mappings": {
            "properties": {
                "office": { "type": "geo_point" },
                "time": { "type": "date" },
            },
        },
    },
    "recordings": {
        "settings": {
            "index": {
                "number_of_shards": 1,
                "number_of_replicas": replicas[0],
            },
        },
        "mappings": {
            "properties": {
                "office": { "type": "geo_point" },
                "time": { "type": "date" },
            },
        },
    },
    "algorithms"+officestr: {
        "settings": {
            "index": {
                "number_of_shards": 1,
                "number_of_replicas": replicas[1],
            },
        },
        "mappings": {
            "properties": {
                "office": { "type": "geo_point" },
            },
        },
    },
    "analytics"+officestr: {
        "settings": {
            "index": {
                "number_of_shards": 1,
                "number_of_replicas": replicas[1],
            },
        },
        "mappings": {
            "properties": {
                "office": { "type": "geo_point" },
                "location": { "type": "geo_point" },
                "time": { "type": "date" },
                "objects": { "type": "nested" },
            },
        },
    },
    "analytics": {
        "settings": {
            "index": {
                "number_of_shards": 1,
                "number_of_replicas": replicas[0],
            },
        },
        "mappings": {
            "properties": {
                "office": { "type": "geo_point" },
                "location": { "type": "geo_point" },
                "time": { "type": "date" },
                "objects": { "type": "nested" },
            },
        },
    },
    "alerts"+officestr: {
        "settings": {
            "index": {
                "number_of_shards": 1,
                "number_of_replicas": replicas[1],
            },
        },
        "mappings": {
            "properties": {
                "time": { "type": "date" },
                "location": { "type": "geo_point" },
                "office": { "type": "geo_point" },
            },
        },
    },
    "services"+officestr: {
        "settings": {
            "index": {
                "number_of_shards": 1,
                "number_of_replicas": replicas[1],
            },
        },
        "mappings": {
            "properties": {
                "office": { "type": "geo_point" },
            },
        },
    },
}

while True:
    try:
        # delete office specific indexes (to start the office afresh)
        for index in settings:
            if index.endswith(officestr):
                print("Delete index "+index , flush=True)
                r=requests.delete(dbhost+"/"+index)

        # initialize db index settings
        _include_type_name={"include_type_name":"false"}
        for index in settings:
            print("Initialize index "+index, flush=True)
            host=dbhost if index.endswith(officestr) else dbchost
            r=requests.put(host+"/"+index,json=settings[index],params=_include_type_name)
            print(r.json(), flush=True)

        officeinfo=Provision(officestr)

        print("Register office {}".format(office), flush=True)
        dbo=DBIngest(index="offices",office="",host=dbchost)
        dbo.ingest(officeinfo, id1=officestr)
        break

    except Exception as e:
        print(traceback.format_exc(), flush=True)
        print("Waiting for DB...", flush=True)

    time.sleep(1)

print("DB Initialized", flush=True)
r=requests.put(dbhost+"/startup"+officestr)

while True:
    time.sleep(10000)

