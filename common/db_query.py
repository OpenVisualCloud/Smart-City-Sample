#!/usr/bin/python3

from db_common import DBCommon
from dsl_yacc import compile, check_nested_label
from language_dsl import text
import json

class DBQuery(DBCommon):
    def __init__(self, index, office, host):
        super(DBQuery,self).__init__(index, office, host)
        self._error=text["query error"]

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

    def _spec_from_index(self):
        spec={"nested":[],"types":{}}
        r=self._request(self._requests.get,self._host+"/"+self._index+"/_mapping",params=self._include_type_name)
        for index1 in r: 
            self._spec_from_mapping(spec,"",r[index1]["mappings"]["properties"])
        return spec

    def search(self, queries, size=10000, spec=None):
        if spec is None: spec=self._spec_from_index()
        dsl=compile(queries,spec)
        r=self._request(self._requests.post,self._host+"/"+self._index+"/_search",json={"query":dsl,"size":size, "seq_no_primary_term": True})
        for x in r["hits"]["hits"]:
            yield x

    def count(self, queries, spec=None):
        if spec is None: spec=self._spec_from_index()
        dsl={ "query": compile(queries,spec) }
        r=self._request(self._requests.post,self._host+"/"+self._index+"/_count",json=dsl)
        return r["count"]

    def stats(self, queries, fields, spec=None):
        if spec is None: spec=self._spec_from_index()
        dsl=compile(queries,spec)
        query={"query":dsl,"aggs":{},"size":0}
        for field in fields:
            nested,var=check_nested_label(spec,field)
            # nested aggs
            aggs={"stats":{"field":var, "missing":0}}
            if nested: 
                for nest1 in nested:
                    aggs={"nested":{"path":nest1},"aggs":{field:aggs}}
            query["aggs"][field]=aggs
        r=self._request(self._requests.post,self._host+"/"+self._index+"/_search",json=query)
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

    def _bucketize(self, queries, fields, size, spec):
        dsl=compile(queries,spec) if queries else {"match_all":{}} 
        dsl={"query":dsl,"aggs":{},"size":0}

        for field in fields:
            nested,var=check_nested_label(spec,field)

            # replace text field with field.keyword
            if "types" in spec:
                if var in spec["types"]:
                    if spec["types"][var]=="text":
                        var=var+".keyword"
            # nested aggs
            aggs={"terms":{"field":var, "size":size}}
            if nested: 
                for nest1 in nested:
                    aggs={"nested":{"path":nest1},"aggs":{nest1:aggs}}
            dsl["aggs"][field]=aggs

        # bucketize
        r=self._request(self._requests.post,self._host+"/"+self._index+"/_search",json=dsl)

        # summariz results
        buckets={}
        aggs=r["aggregations"]
        for field in aggs:
            buckets[field]={}
            self._scan_bucket(buckets[field],aggs[field])
        return buckets

    def bucketize(self, queries, fields, size=25, spec=None):
        if spec is None: spec=self._spec_from_index()
        return self._bucketize(queries,fields,size,spec)

    def update(self, _id, info, seq_no=None, primary_term=None):
        options={}
        if seq_no is not None: options["if_seq_no"]=seq_no
        if primary_term is not None: options["if_primary_term"]=primary_term
        return self._request(self._requests.post,self._host+"/"+self._index+"/_doc/"+_id+"/_update",params=options,json={"doc":info})  #ES6.8
        return self._request(self._requests.post,self._host+"/"+self._index+"/_update/"+_id,params=options,json={"doc":info})  #ES7.4

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
            self._request(self._requests.post,self._host+"/_bulk",data=cmds,headers={"content-type":"application/x-ndjson"})

    def hints(self, size=50, spec=None):
        if spec is None: spec=self._spec_from_index()
        keywords={}
        fields=[]

        if "types" in spec:
            types=spec["types"]
            for var in types:
                keywords[var]={"type":types[var]}
                if types[var]=="text": 
                    if var!="md5" and var!="passcode": #exclude from hints
                        fields.append(var)

        values=self._bucketize(None,fields,size,spec)
        for var in values:
            keywords[var]["values"]=list(values[var].keys())
        return keywords
