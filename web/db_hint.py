#!/usr/bin/python3

import requests
import json
import re

class DBHint(object):
    def __init__(self, index, office, host):
        super(DBHint,self).__init__()
        self._host=host
        indexes=index.split(",")
        if isinstance(office,list): office=re.sub(r'[.-]','$','$'.join(map(str,office)))
        self._index=indexes[0]+"$"+office
        self._type="_doc"

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
