#!/usr/bin/python3

import requests
import json

class DBIngest(object):
    def __init__(self, index, host="http://database:9200"):
        super(DBIngest,self).__init__()
        self._host=host
        self._index=index
        self._type="_doc"
        self._mappings={
            "sensors": {
                "mappings": {
                    self._type: {
                        "properties": {
                            "office": { "type": "geo_point", },
                            "location": { "type": "geo_point", },
                        },
                    },
                },
            },
            "recordings": {
                "mappings": {
                    self._type: {
                        "properties": {
                            "office": { "type": "geo_point" },
                            "time": { "type": "date" },
                            "streams": { "type": "nested" },
                        },
                    },
                },
            },
            "algorithms": {
                "mappings": {
                    self._type: {
                        "properties": {
                            "office": { "type": "geo_point" },
                        },
                    },
                },
            },
            "analytics": {
                "mappings": {
                    self._type: {
                        "properties": {
                            "office": { "type": "geo_point" },
                            "time": { "type": "date" },
                            "objects": { "type": "nested" },
                            "heatmap": { 
                                "properties": {
                                    "location": { "type": "geo_point" },
                                },
                            },
                        },
                    },
                },
            },
            "alerts": {
                "mappings": {
                    self._type: {
                        "properties": {
                            "time": { "type": "date" },
                            "office": { "type": "geo_point" },
                        },
                    },
                },
            },
        }

    def _check_error(self, r):
        if r.status_code==200 or r.status_code==201: return
        try:
            reason=r.json()["error"]["reason"]
        except:
            r.raise_for_status()
        raise Exception(reason)

    def ingest_bulk(self, bulk, batch=500):
        ''' save bulk data to the database
            bulk: list of bulk data
        '''
        self._check_mapping()
        while bulk:
            cmds=[]
            for b in bulk[0:batch]:
                cmds.append({"index":{"_index":self._index,"_type":self._type}})
                cmds.append(b)
            bulk=bulk[batch:]
                
            cmds="\n".join([json.dumps(x) for x in cmds])+"\n"
            r=requests.post(self._host+"/_bulk",data=cmds,headers={"content-type":"application/x-ndjson"})
            self._check_error(r)
        
    def ingest(self, info):
        self._check_mapping()
        r=requests.post(self._host+"/"+self._index+"/"+self._type,json=info)
        self._check_error(r)
        return r.json()

    def _check_mapping(self):
        if self._index not in self._mappings: return
        r=requests.put(self._host+"/"+self._index,json=self._mappings.pop(self._index))
        if r.status_code!=200 and r.status_code!=201:
            print(r.text,flush=True)

    def update(self, _id, info, version=None):
        self._check_mapping()
        options={} if version is None else { "version": version }
        r=requests.post(self._host+"/"+self._index+"/"+self._type+"/"+_id+"/_update",params=options,json={"doc":info})
        self._check_error(r)
        return r.json()

    def delete(self, _id):
        r=requests.delete(self._host+"/"+self._index+"/"+self._type+"/"+_id,headers={'Content-Type':'application/json'})
        self._check_error(r)
        return r.json()
