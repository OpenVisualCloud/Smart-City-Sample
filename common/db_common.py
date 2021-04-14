#!/usr/bin/python3

from threading import Event
import requests
import string
import re

class DBCommon(object):
    def __init__(self, index, office, host):
        super(DBCommon,self).__init__()
        if isinstance(office,list): office='_'+('_'.join(map(str,office)))
        if isinstance(office,dict): office='_'+str(office["lat"])+'_'+str(office["lon"])
        self._office=re.sub(r'\.?0*_',r'_',re.sub(r'\.?0*$',r'',office)).translate(str.maketrans("-.","nd"))
        self._index=index+self._office
        self._include_type_name={"include_type_name":"false"}
        self._host=host
        self._error=""
        self._requests=requests.Session()

    def office(self):
        return self._office

    def _request(self, op, *args, **kwargs):
        try:
            r=op(*args, **kwargs)
            if r.status_code==200 or r.status_code==201: return r.json()
            print("Exception: {}".format(r.json()), flush=True)
        except Exception as e:
            print("Exception: {}".format(e), flush=True)
        raise Exception(self._error)

    def delete(self, _id):
        return self._request(self._requests.delete,self._host+"/"+self._index+"/_doc/"+_id,headers={'Content-Type':'application/json'})

    def wait(self, stop=Event()):
        while not stop.is_set():
            try:
                r=self._request(self._requests.get, self._host+"/sensors"+self._office+"/_doc/_search",json={"query":{"term":{"type.keyword":"startup"}},"size":1})
                if r["hits"]["hits"]: return stop
            except:
                pass
            print("Waiting for DB...", flush=True)
            stop.wait(1)

    def health(self):
        r=self._request(self._requests.get,self._host+"/_cluster/health")
        return r["status"]=="green" or r["status"]=="yellow"
