#!/usr/bin/python3

from dsl_yacc import compile, check_nested_label
from language_dsl import text
import traceback
import requests
import time
import json

class DBQuery(object):
    def __init__(self, index, office, host):
        super(DBQuery,self).__init__()
        self._host=host
        indexes=index.split(",")
        if isinstance(office,list): office='$'+('$'.join(map(str,office)))
        if isinstance(office,dict): office='$'+str(office["lat"])+"$"+str(office("lon"))
        self._index=indexes[0]+office
        self._include_type_name={"include_type_name":"false"}
        self._where=indexes[1]+office if len(indexes)>1 else None

    def _request(self, op, *args, **kwargs):
        try:
            r=op(*args, **kwargs)
            if r.status_code==200 or r.status_code==201: return r.json()
            print("Exception: "+str(r.json()["error"]["reason"]), flush=True)
        except:
            print(traceback.format_exc(), flush=True)
        raise Exception(text["query error"])

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

        r=self._request(requests.get,self._host+"/"+index+"/_mapping",params=self._include_type_name)
        for index1 in r: 
            self._spec_from_mapping(specs[-1],"",r[index1]["mappings"]["properties"])

    def _specs(self):
        specs=[]
        self._spec_from_index(specs,self._index)
        if self._where: self._spec_from_index(specs,self._where)
        return specs

    def search(self, queries, size=10000, where_size=200):
        dsl=compile(queries,self._specs())
        query=dsl[0]
        if len(dsl)>1:
            r=self._request(requests.post,self._host+"/"+self._where+"/_search",json={"query":dsl[1],"size":0,"aggs":{ "recording": { "terms": { "field": "recording.keyword", "min_doc_count": 1, "size": where_size }}}})
            ids=[x["key"] for x in r["aggregations"]["recording"]["buckets"]]
            query={"bool":{"must":[query,{"ids":{"values":ids}}]}}
        r=self._request(requests.post,self._host+"/"+self._index+"/_search",json={"query":query,"size":size, "seq_no_primary_term": True})
        for x in r["hits"]["hits"]:
            yield x

    def count(self,queries):
        dsl={ "query": compile(queries,self._specs())[0] }
        r=self._request(requests.post,self._host+"/"+self._index+"/_count",json=dsl)
        return r["count"]

    def stats(self, queries, fields):
        specs=self._specs()
        dsl=compile(queries,specs)
        query={"query":dsl[0],"aggs":{},"size":0}
        for field in fields:
            nested,var=check_nested_label(specs[0],field)
            # nested aggs
            aggs={"stats":{"field":var, "missing":0}}
            if nested: 
                for nest1 in nested:
                    aggs={"nested":{"path":nest1},"aggs":{field:aggs}}
            query["aggs"][field]=aggs
        r=self._request(requests.post,self._host+"/"+self._index+"/_search",json=query)
        aggs=r["aggregations"]
        data={}
        for field in fields:
            values=aggs
            while field in values: 
                values=values[field]
            data[field]=values
        return data

    def _scan_bucket(self, buckets, r):
        for k in r:
            if k=="buckets":
                for x in r[k]:
                    buckets[x["key"]]=x["doc_count"]
                continue
            if isinstance(r[k],dict):
                self._scan_bucket(buckets,r[k])

    def _bucketize(self, queries, fields, size, specs):
        if not specs: specs=self._specs()

        dsl=compile(queries,specs)[0] if queries else {"match_all":{}} 
        dsl={"query":dsl,"aggs":{},"size":0}

        for field in fields:
            nested,var=check_nested_label(specs[0],field)

            # replace text field with field.keyword
            if "types" in specs[0]:
                if var in specs[0]["types"]:
                    if specs[0]["types"][var]=="text":
                        var=var+".keyword"
            # nested aggs
            aggs={"terms":{"field":var, "size":size}}
            if nested: 
                for nest1 in nested:
                    aggs={"nested":{"path":nest1},"aggs":{nest1:aggs}}
            dsl["aggs"][field]=aggs

        # bucketize
        r=self._request(requests.post,self._host+"/"+self._index+"/_search",json=dsl)

        # summariz results
        buckets={}
        aggs=r["aggregations"]
        for field in aggs:
            buckets[field]={}
            self._scan_bucket(buckets[field],aggs[field])
        return buckets

    def bucketize(self, queries, fields, size=25):
        specs=self._specs()
        return self._bucketize(queries,fields,size,specs)

    def update(self, _id, info, seq_no=None, primary_term=None):
        options={}
        if seq_no is not None: options["if_seq_no"]=seq_no
        if primary_term is not None: options["if_primary_term"]=primary_term
        return self._request(requests.post,self._host+"/"+self._index+"/_doc/"+_id+"/_update",params=options,json={"doc":info})  #ES6.8
        return self._request(requests.post,self._host+"/"+self._index+"/_update/"+_id,params=options,json={"doc":info})  #ES7.4

    def update_bulk(self, updates, batch=500):
        """ update in a bulk:
            updates: list of [_id, _doc]
        """
        while updates:
            cmds=[]
            for u in updates[0:batch]:
                cmds.append({ "update": {
                    "_index":self._index,
                    "_type":"_doc", #ES6.8
                    "_id": u[0],
                }})
                cmds.append({ "doc": u[1] })
            updates=updates[batch:]

            cmds="\n".join([json.dumps(x) for x in cmds])+"\n"
            self._request(requests.post,self._host+"/_bulk",data=cmds,headers={"content-type":"application/x-ndjson"})

    def delete(self, _id):
        return self._request(requests.delete,self._host+"/"+self._index+"/_doc/"+_id,headers={'Content-Type':'application/json'})

    def hints(self, size=50):
        specs=self._specs()
        keywords={}
        fields=[]

        types=specs[0]["types"]
        for var in types:
            keywords[var]={"type":types[var]}
            if types[var]=="text": 
                fields.append(var)

        values=self._bucketize(None,fields,size,specs)
        for var in values:
            keywords[var]["values"]=list(values[var].keys())
        return keywords
