#!/usr/bin/python3

from signal import SIGTERM, signal
from db_ingest import DBIngest
from provision import Provision
from office import RegisterOffice
import traceback
import requests
import time
import os
import json
import re

dbhost=os.environ["DBHOST"]
dbchost=os.environ["DBCHOST"]
office=list(map(float,os.environ["OFFICE"].split(",")))

def quit_service():
    exit(143)

signal(SIGTERM, quit_service)
officestr=DBIngest.office_str(office)

settings={
    "offices": {
        "settings": {
            "index": {
                "number_of_shards": 1,
                "number_of_replicas": 0,
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
                "number_of_replicas": 0,
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
                "number_of_replicas": 0,
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
                "number_of_replicas": 0,
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
                "number_of_replicas": 0,
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
                "number_of_replicas": 0,
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
                "number_of_replicas": 0,
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
                "number_of_replicas": 0,
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
                "number_of_replicas": 0,
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
                "number_of_replicas": 0,
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
                "number_of_replicas": 0,
            },
        },
        "mappings": {
            "properties": {
                "office": { "type": "geo_point" },
            },
        },
    },
}

# wait until DB is ready
while True:
    try:
        r=requests.get(dbhost+"/_cluster/health").json()
        if r["status"]=="green" or r["status"]=="yellow": break
    except:
        print("Waiting for DB...", flush=True)
    time.sleep(1)
    
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
        RegisterOffice(officestr, officeinfo)
        break

    except Exception as e:
        print(traceback.format_exc(), flush=True)
        print("Waiting for DB...", flush=True)

    time.sleep(1)

print("DB Initialized", flush=True)
r=requests.put(dbhost+"/startup"+officestr)

while True:
    time.sleep(10000)

