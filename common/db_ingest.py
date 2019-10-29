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
        r=requests.put(self._host+"/"+self._index+"/"+self._type+"/"+id1,json=info) if id1 else requests.post(self._host+"/"+self._index+"/"+self._type,json=info)
        self._check_error(r)
        return r.json()

    def update(self, _id, info, seq_no=None, primary_term=None):
        options={}
        if seq_no: options["if_seq_no"]=seq_no
        if primary_term: options["if_primary_term"]=primary_term
        r=requests.post(self._host+"/"+self._index+"/"+self._type+"/"+_id+"/_update",params=options,json={"doc":info})
        self._check_error(r)
        return r.json()

    def delete(self, _id):
        r=requests.delete(self._host+"/"+self._index+"/"+self._type+"/"+_id,headers={'Content-Type':'application/json'})
        self._check_error(r)
        return r.json()
