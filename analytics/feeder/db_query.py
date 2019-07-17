#!/usr/bin/python3

import requests
import time
import json
from dsl_yacc import compile
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

    def _get_keywords(self, prefix, mapping):
        for p in mapping:
            keyword = p if not prefix else prefix + "." + p
            if "properties" in mapping[p]:
                for keyword1 in self._get_keywords(keyword, mapping[p]["properties"]):
                    yield (keyword1[0], keyword1[1])
            if "type" in mapping[p]:
                if mapping[p]["type"] != "nested":
                    yield (keyword, mapping[p]["type"])

    def hints(self, size=50):
        keywords = {}
        r=requests.get(self._host+"/"+self._index+"/"+self._type+"/_mapping")
        if r.status_code == 200:
            r=r.json()
            for index1 in r:
                for x in list(self._get_keywords(None, r[index1]["mappings"][self._type]["properties"])):
                    keywords[x[0]] = {"type": x[1]}

        # TODO: nested aggs
        aggs = {}
        for k in keywords:
            if keywords[k]["type"] != "text": continue
            aggs[k] = {"terms": {"field": k + ".keyword", "size": size}}

        cmds = [{"index": self._index, "type": self._type}]
        cmds.append({"size": 0, "aggs": aggs})
        cmds="\n".join([json.dumps(x) for x in cmds])+"\n"
        r=requests.post(self._host+"/_msearch",data=cmds,headers={"content-type":"application/x-ndjson"})
        if r.status_code == 200:
            for response in r.json()["responses"]:
                if response["status"] != 200: continue
                for k in response["aggregations"]:
                    values = {}
                    for value in [b["key"] for b in response["aggregations"][k]["buckets"] if b["key"]]:
                        if value: values[value] = True
                    keywords[k]["values"] = list(values.keys())
        return keywords
