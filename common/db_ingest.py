#!/usr/bin/python3

from db_common import DBCommon
from language_dsl import text
import json

class DBIngest(DBCommon):
    def __init__(self, index, office, host):
        super(DBIngest,self).__init__(index,office,host)
        self._error=text["ingest error"]

    def ingest_bulk(self, bulk, batch=500, refresh="false"):
        ''' save bulk data to the database
            bulk: list of bulk data
        '''
        while bulk:
            cmds=[]
            for b in bulk[0:batch]:
                cmds.append({
                    "index":{
                        "_index":self._index,
                        "_type":"_doc",  # ES6.8
                    },
                })
                cmds.append(b)
            bulk=bulk[batch:]
                
            cmds="\n".join([json.dumps(x) for x in cmds])+"\n"
            self._request(self._requests.post,self._host+"/_bulk?refresh="+refresh,data=cmds,headers={"content-type":"application/x-ndjson"})
        
    def ingest(self, info, id1=None, refresh="false"):
        if id1:
            return self._request(self._requests.put,self._host+"/"+self._index+"/_doc/"+id1+"?refresh="+refresh,json=info)
        else:
            return self._request(self._requests.post,self._host+"/"+self._index+"/_doc?refresh="+refresh,json=info)

    def update(self, _id, info, seq_no=None, primary_term=None):
        options={}
        if seq_no is not None: options["if_seq_no"]=seq_no
        if primary_term is not None: options["if_primary_term"]=primary_term
        return self._request(self._requests.post,self._host+"/"+self._index+"/_doc/"+_id+"/_update",params=options,json={"doc":info})  #ES6.8
        #return self._request(self._requests.post,self._host+"/"+self._index+"/_update/"+_id,params=options,json={"doc":info})  #ES7.4
