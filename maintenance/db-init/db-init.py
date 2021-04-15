#!/usr/bin/python3

from signal import SIGTERM, signal
from db_ingest import DBIngest
from provision import Provision
from configuration import env
import traceback
import requests
import time
import json
import re

dbhost=env["DBHOST"]
dbchost=env.get("DBCHOST",None)
office=list(map(float,env["OFFICE"].split(",")))
replicas=list(map(int,env["REPLICAS"].split(",")))

def quit_service():
    exit(143)

signal(SIGTERM, quit_service)

# wait until DB is ready
dbs=DBIngest(index="sensors", office=office, host=dbhost)
while True:
    try:
        if dbs.health(): break
    except:
        print("Waiting for DB...", flush=True)
    time.sleep(1)
    
officestr=dbs.office()
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
                "rtmpid": {
                    "type" : "text",
                    "fields" : {
                        "keyword" : {
                            "type" : "keyword",
                            "ignore_above" : 256,
                        },
                    },
                },
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
                "type": {
                    "type" : "text",
                    "fields" : {
                        "keyword" : {
                            "type" : "keyword",
                            "ignore_above" : 256,
                        },
                    },
                },
                "subtype": {
                    "type" : "text",
                    "fields" : {
                        "keyword" : {
                            "type" : "keyword",
                            "ignore_above" : 256,
                        },
                    },
                },
                "algorithm": {
                    "type" : "text",
                    "fields" : {
                        "keyword" : {
                            "type" : "keyword",
                            "ignore_above" : 256,
                        },
                    },
                },
                "address": {
                    "type" : "text",
                    "fields" : {
                        "keyword" : {
                            "type" : "keyword",
                            "ignore_above" : 256,
                        },
                    },
                },
                "mnth": { "type": "float" },
                "alpha": { "type": "float" },
                "fovh": { "type": "float" },
                "fovv": { "type": "float" },
                "theta": { "type": "float" },
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
                "type": {
                    "type" : "text",
                    "fields" : {
                        "keyword" : {
                            "type" : "keyword",
                            "ignore_above" : 256,
                        },
                    },
                },
                "subtype": {
                    "type" : "text",
                    "fields" : {
                        "keyword" : {
                            "type" : "keyword",
                            "ignore_above" : 256,
                        },
                    },
                },
                "algorithm": {
                    "type" : "text",
                    "fields" : {
                        "keyword" : {
                            "type" : "keyword",
                            "ignore_above" : 256,
                        },
                    },
                },
                "address": {
                    "type" : "text",
                    "fields" : {
                        "keyword" : {
                            "type" : "keyword",
                            "ignore_above" : 256,
                        },
                    },
                },
                "mnth": { "type": "float" },
                "alpha": { "type": "float" },
                "fovh": { "type": "float" },
                "fovv": { "type": "float" },
                "theta": { "type": "float" },
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

_requests=requests.Session()
while True:
    try:
        # delete office specific indexes (to start the office afresh)
        for index in settings:
            if index.endswith(officestr):
                print("Delete index "+index , flush=True)
                r=_requests.delete(dbhost+"/"+index)

        # initialize db index settings
        _include_type_name={"include_type_name":"false"}
        for index in settings:
            print("Initialize index "+index, flush=True)
            host=dbhost if index.endswith(officestr) else dbchost
            if host:
                r=_requests.put(host+"/"+index,json=settings[index],params=_include_type_name)
                print(r.json(), flush=True)

        officeinfo=Provision(officestr)

        if dbchost:
            print("Register office {}".format(office), flush=True)
            dbo_c=DBIngest(index="offices",office="",host=dbchost)
            dbo_c.ingest(officeinfo, id1=officestr)

        print("Signal starting up", flush=True)
        dbs.ingest({"type":"startup"})
        break

    except Exception as e:
        print(traceback.format_exc(), flush=True)
        print("Waiting for DB...", flush=True)

    time.sleep(1)

print("DB Initialized", flush=True)

while True:
    time.sleep(10000)

