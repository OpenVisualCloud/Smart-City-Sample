#!/usr/bin/python3

import requests
import time
import json
from dsl_yacc import compile, check_nested_label
import re

class DBQuery(object):
    def __init__(self, index, office, host):
        super(DBQuery,self).__init__()
        self._host=host
        indexes=index.split(",")
        if isinstance(office,list): office=re.sub(r'[.-]','$','$'.join(map(str,office)))
        self._index=indexes[0]+"$"+office
        self._type="_doc"
        self._where=indexes[1]+"$"+office if len(indexes)>1 else None

    def _check_error(self, r):
        if r.status_code==200 or r.status_code==201: return
        try:
            reason=r.json()["error"]["reason"]
        except:
            r.raise_for_status()
        raise Exception(reason)

    def _spec_from_mapping(self, spec, prefix, properties):
        for field in properties:
            if "type" in properties[field]:
                type1=properties[field]["type"]
                if type1=="nested":
                    if prefix+field not in spec["nested"]: 
                        spec["nested"].append(prefix+field)
                else:
                    spec["types"][prefix+field]=type1
            if "properties" in properties[field]:
                self._spec_from_mapping(spec, prefix+field+".", properties[field]["properties"])

    def _spec_from_index(self, specs, index):
        specs.append({"nested":[],"types":{}})
        r=requests.get(self._host+"/"+index+"/"+self._type+"/_mapping")
        if r.status_code!=200: return
        r=r.json()
        for index1 in r: 
            self._spec_from_mapping(specs[-1],"",r[index1]["mappings"][self._type]["properties"])

    def _specs(self):
        specs=[]
        self._spec_from_index(specs,self._index)
        if self._where: self._spec_from_index(specs,self._where)
        return specs

    def search(self, queries, size=10000, where_size=200):
        dsl=compile(queries,self._specs())
        query=dsl[0]
        if len(dsl)>1:
            r=requests.post(self._host+"/"+self._where+"/"+self._type+"/_search",json={"query":dsl[1],"size":0,"aggs":{ "recording": { "terms": { "field": "recording.keyword", "min_doc_count": 1, "size": where_size }}}})
            self._check_error(r)
            ids=[x["key"] for x in r.json()["aggregations"]["recording"]["buckets"]]
            query={"bool":{"must":[query,{"ids":{"values":ids}}]}}
        r=requests.post(self._host+"/"+self._index+"/"+self._type+"/_search",json={"query":query,"size":size,"version":True})
        self._check_error(r)
        for x in r.json()["hits"]["hits"]:
            yield x

    def count(self,queries):
        dsl={ "query": compile(queries,self._specs())[0] }
        r=requests.post(self._host+"/"+self._index+"/"+self._type+"/_count",json=dsl)
        self._check_error(r)
        return r.json()["count"]

    def bucketize(self, queries, field):
        specs=self._specs()
        nested,var=check_nested_label(specs[0],field)
        if "types" in specs[0]:
            if var in specs[0]["types"]:
                if specs[0]["types"][var]=="text":
                    var=var+".keyword"
        aggs={"terms":{"field":var}}
        if nested: aggs={"nested":{"path":nested[0]},"aggs":{"agg2":aggs}}
        dsl={"query":compile(queries,specs)[0],"aggs":{"agg1":aggs},"size":0}
        r=requests.post(self._host+"/"+self._index+"/"+self._type+"/_search",json=dsl)
        self._check_error(r)
        r=r.json()["aggregations"]["agg1"]
        if "buckets" not in r: r=r["agg2"]
        buckets={}
        for x in r["buckets"]:
            buckets[x["key"]]=x["doc_count"]
        return buckets

    def update(self, _id, info, version=None):
        options={} if version is None else { "version": version }
        r=requests.post(self._host+"/"+self._index+"/"+self._type+"/"+_id+"/_update",params=options,json={"doc":info})
        self._check_error(r)
        return r.json()

    def update_bulk(self, updates, batch=500):
        """ update in a bulk:
            updates: list of [_id, _doc]
        """
        while updates:
            cmds=[]
            for u in updates[0:batch]:
                cmds.append({ "update": {
                    "_index":self._index,
                    "_type":self._type,
                    "_id": u[0],
                }})
                cmds.append({ "doc": u[1] })
            updates=updates[batch:]

            cmds="\n".join([json.dumps(x) for x in cmds])+"\n"
            r=requests.post(self._host+"/_bulk",data=cmds,headers={"content-type":"application/x-ndjson"})
            self._check_error(r)

    def delete(self, _id):
        r=requests.delete(self._host+"/"+self._index+"/"+self._type+"/"+_id,headers={'Content-Type':'application/json'})
        self._check_error(r)
        return r.json()
