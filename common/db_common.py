#!/usr/bin/python3

from threading import Event
import requests
import string
import re

class DBCommon(object):
    def __init__(self, index, office, host, remote=False):
        super(DBCommon,self).__init__()
        self._host=host
        ostr=self.office_str(office)
        self._index=ostr[1:]+":"+index+ostr if remote else index+ostr
        self._include_type_name={"include_type_name":"false"}
        self._error=""

    @staticmethod
    def office_str(office):
        if isinstance(office,list): office='_'+('_'.join(map(str,office)))
        if isinstance(office,dict): office='_'+str(office["lat"])+'_'+str(office["lon"])
        return re.sub(r'\.?0*_',r'_',re.sub(r'\.?0*$',r'',office)).translate(str.maketrans("-.","nd"))

    def _request(self, op, *args, **kwargs):
        try:
            r=op(*args, **kwargs)
            if r.status_code==200 or r.status_code==201: return r.json()
            print("Exception: "+str(r.json()["error"]["reason"]), flush=True)
        except Exception as e:
            print("Exception: {}".format(e), flush=True)
        raise Exception(self._error)

    def delete(self, _id):
        return self._request(requests.delete,self._host+"/"+self._index+"/_doc/"+_id,headers={'Content-Type':'application/json'})

    def wait(self, stop=Event()):
        officestr="_"+"_".join(self._index.split("_")[1:])
        while not stop.is_set():
            try:
                r=requests.get(self._host+"/startup"+officestr)
                if r.status_code==200: return stop
            except:
                pass
            print("Waiting for DB...", flush=True)
            stop.wait(1)
