#!/usr/bin/python3

import requests
import json

class DBIngest(object):
    def __init__(self, index, office, host):
        super(DBIngest,self).__init__()
        self._host=host
        if isinstance(office,list): office='$'+('$'.join(map(str,office)))
        self._index=index+office
        self._type="_doc"
        self._mappings={
            "offices": {
                "mappings": {
                    self._type: {
                        "properties": {
                            "office": { "type": "geo_point", },
                        },
                    },
                },
            },
            "sensors"+office: {
                "mappings": {
                    self._type: {
                        "properties": {
                            "office": { "type": "geo_point", },
                            "location": { "type": "geo_point", },
                        },
                    },
                },
            },
            "recordings"+office: {
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
            "algorithms"+office: {
                "mappings": {
                    self._type: {
                        "properties": {
                            "office": { "type": "geo_point" },
                        },
                    },
                },
            },
            "analytics"+office: {
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
            "alerts"+office: {
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
        
    def ingest(self, info, id1=None):
        self._check_mapping()
        r=requests.put(self._host+"/"+self._index+"/"+self._type+"/"+id1,json=info) if id1 else requests.post(self._host+"/"+self._index+"/"+self._type,json=info)
        self._check_error(r)
        return r.json()

    def _check_mapping(self):
        if self._index in self._mappings:
            requests.put(self._host+"/"+self._index,json=self._mappings[self._index])
            # remove from mapping only if there is no exception after updating mapping
            self._mappings.pop(self._index)

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
