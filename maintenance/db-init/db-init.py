#!/usr/bin/python3

from signal import SIGTERM, signal
from db_ingest import DBIngest
import requests
import time
import os
import json

dbhost=os.environ["DBHOST"]
office=list(map(float,os.environ["OFFICE"].split(",")))
zone=os.environ["ZONE"]

def quit_service():
    exit(143)

signal(SIGTERM, quit_service)
officestr='$'+('$'.join(map(str,office)))

def defaults():
    return {
        "offices": {
            "settings": {
                "index.routing.allocation.include.zone": "cloud",
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
                "index.routing.allocation.include.zone": "cloud,"+zone,
                "index": {
                    "number_of_shards": 1,
                    "number_of_replicas": 1,
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
                "index.routing.allocation.include.zone": "cloud,"+zone,
                "index": {
                    "number_of_shards": 1,
                    "number_of_replicas": 1,
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
                "index.routing.allocation.include.zone": "cloud",
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
                "index.routing.allocation.include.zone": "cloud,"+zone,
                "index": {
                    "number_of_shards": 1,
                    "number_of_replicas": 1,
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
                "index.routing.allocation.include.zone": "cloud",
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
                "index.routing.allocation.include.zone": "cloud,"+zone,
                "index": {
                    "number_of_shards": 1,
                    "number_of_replicas": 1,
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
                "index.routing.allocation.include.zone": "cloud,"+zone,
                "index": {
                    "number_of_shards": 1,
                    "number_of_replicas": 1,
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
                "index.routing.allocation.include.zone": "cloud",
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
                "index.routing.allocation.include.zone": "cloud,"+zone,
                "index": {
                    "number_of_shards": 1,
                    "number_of_replicas": 1,
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
                "index.routing.allocation.include.zone": "cloud,"+zone,
                "index": {
                    "number_of_shards": 1,
                    "number_of_replicas": 1,
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
    settings=defaults()

    try:
        # delete office specific indexes (to start the office afresh)
        for index in settings:
            if index.endswith(officestr):
                print("Delete index "+index , flush=True)
                requests.delete(dbhost+"/"+index)

        # initialize db index settings
        _include_type_name={"include_type_name":"false"}
        routing_key="index.routing.allocation.include.zone"
        for index in settings:
            print("Initialize index "+index, flush=True)
            routing_value=settings[index]["settings"].pop(routing_key)

            r=requests.put(dbhost+"/"+index,json=settings[index],params=_include_type_name)
            r=requests.put(dbhost+"/"+index+"/_settings",json={ routing_key: routing_value })

        import provision
        break

    except Exception as e:
        print("Exception: {}".format(e), flush=True)
        print("Waiting for DB...", flush=True)

    time.sleep(1)

print("DB Initialized", flush=True)
while True:
    time.sleep(10000)

