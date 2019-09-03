#!/usr/bin/python3

import requests
import time
import os

dbhost=os.environ["DBHOST"]
office='$'+('$'.join(map(str,map(float,os.environ["OFFICE"].split(",")))))
_type="_doc"
settings={
    "offices": {
        "settings": {
            "index": {
                "number_of_shards": 1,
                "number_of_replicas": 1,
            },
        },
        "mappings": {
            _type: {
                "properties": {
                    "office": { "type": "geo_point", },
                },
            },
        },
    },
    "sensors"+office: {
        "settings": {
            "index": {
                "number_of_shards": 1,
                "number_of_replicas": 1,
            },
        },
        "mappings": {
            _type: {
                "properties": {
                    "office": { "type": "geo_point", },
                    "location": { "type": "geo_point", },
                },
            },
        },
    },
    "recordings"+office: {
        "settings": {
            "index": {
                "number_of_shards": 1,
                "number_of_replicas": 1,
            },
        },
        "mappings": {
            _type: {
                "properties": {
                    "office": { "type": "geo_point" },
                    "time": { "type": "date" },
                    "streams": { "type": "nested" },
                },
            },
        },
    },
    "algorithms"+office: {
        "settings": {
            "index": {
                "number_of_shards": 1,
                "number_of_replicas": 1,
            },
        },
        "mappings": {
            _type: {
                "properties": {
                    "office": { "type": "geo_point" },
                },
            },
        },
    },
    "analytics"+office: {
        "settings": {
            "index": {
                "number_of_shards": 1,
                "number_of_replicas": 1,
            },
        },
        "mappings": {
            _type: {
                "properties": {
                    "office": { "type": "geo_point" },
                    "time": { "type": "date" },
                    "objects": { "type": "nested" },
                },
            },
        },
    },
    "alerts"+office: {
        "settings": {
            "index": {
                "number_of_shards": 1,
                "number_of_replicas": 1,
            },
        },
        "mappings": {
            _type: {
                "properties": {
                    "time": { "type": "date" },
                    "office": { "type": "geo_point" },
                },
            },
        },
    },
    "services"+office: {
        "settings": {
            "index": {
                "number_of_shards": 1,
                "number_of_replicas": 1,
            },
        },
    },
}

for index in settings:
    while True:
        try:
            r=requests.put(dbhost+"/"+index,json=settings[index])
            break
        except Exception as e:
            print("Exception: "+str(e),flush=True)
            time.sleep(10)
