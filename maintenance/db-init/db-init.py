#!/usr/bin/python3

from db_ingest import DBIngest
import requests
import time
import os
import json

dbhost=os.environ["DBHOST"]
office=list(map(float,os.environ["OFFICE"].split(",")))
zone=os.environ["ZONE"]

officestr='$'+('$'.join(map(str,office)))
settings={
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

# delete office specific indexes (to start the office afresh)
for index in settings:
    if index.endswith(officestr):
        print("Delete index "+index , flush=True)
        while True:
            try:
                r=requests.delete(dbhost+"/"+index)
                if r.status_code==404 or r.status_code==200: break
            except:
                print("Waiting for DB...", flush=True)
            time.sleep(5)

# initialize db index settings
_include_type_name={"include_type_name":"false"}
routing_key="index.routing.allocation.include.zone"
for index in settings:
    print("Initialize index "+index, flush=True)
    routing_value=settings[index]["settings"].pop(routing_key)

    r=requests.put(dbhost+"/"+index,json=settings[index],params=_include_type_name)
    r=requests.put(dbhost+"/"+index+"/_settings",json={ routing_key: routing_value })
