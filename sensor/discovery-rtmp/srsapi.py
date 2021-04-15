#!/usr/bin/python3

import requests
import json

class SRSAPI(object):
    def __init__(self, host, timeout=30):
        super(SRSAPI,self).__init__()
        self._host=host
        self._timeout=timeout
        self._requests=requests.Session()

    def _request(self, op, *args, **kwargs):
        try:
            r=op(*args, **kwargs)
            if r.status_code==200 or r.status_code==201: return r
            print("Exception: "+ r.text, flush=True)
        except Exception as e:
            print("Exception: "+str(e), flush=True)
        raise Exception("SRS Http API error!")

    def list_stream(self):
        uri=self._host+"/api/v1/streams/"
        r=self._request(self._requests.get,uri)
        return r.json()["streams"]

    def get_stream(self,stream=""):
        uri=self._host+"/api/v1/streams/"+str(stream)
        r=self._request(self._requests.get,uri)
        return r.json()["stream"]
