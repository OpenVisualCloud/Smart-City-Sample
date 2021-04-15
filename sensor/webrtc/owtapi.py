#!/usr/bin/python3

from hashlib import sha256
from binascii import b2a_base64
import hmac
import requests
import json
import random
import time

class OWTAPI(object):
    def __init__(self, service='', key='', host="http://localhost:3000",timeout=30):
        super(OWTAPI,self).__init__()
        self._host=host
        self._timeout=timeout
        self._serviceid=service
        self._key=key.encode('utf-8')
        self._requests=requests.Session()

    def _headers(self):
        mauth_realm='MAuth realm=http://marte3.dit.upm.es'
        mauth_signature_method="mauth_signature_method=HMAC_SHA256"
        mauth_serviceid="mauth_serviceid="+self._serviceid
        cnonce=str(random.randint(0,99999))
        mauth_cnonce="mauth_cnonce="+cnonce
        timestamp=str(int(time.time()))
        mauth_timestamp="mauth_timestamp="+timestamp

        tosign=timestamp+","+cnonce
        hash=hmac.new(self._key,tosign.encode('utf-8'), sha256)
        hexdigest=b2a_base64(hash.hexdigest().encode('utf-8')).decode('utf-8')[:-1]
        mauth_signature="mauth_signature="+hexdigest
        return {
            'Authorization': '{},{},{},{},{},{}'.format(mauth_realm,mauth_signature_method,mauth_serviceid,mauth_cnonce,mauth_timestamp,mauth_signature),
        }

    def _request(self, op, *args, **kwargs):
        try:
            r=op(*args, **kwargs)
            if r.status_code==200 or r.status_code==201: return r
            print("Exception: "+ r.text, flush=True)
        except Exception as e:
            print("Exception: "+str(e), flush=True)
        raise Exception("OWTAPI error")

    def create_room(self,name,p_limit=10,i_limit=1):
        _options={"name":name,"options":{"participantLimit":p_limit,"inputLimit":i_limit,"views":[]}}
        uri=self._host+"/v1/rooms"
        r=self._request(self._requests.post,uri,json=_options,headers=self._headers())
        return r.json()["_id"]

    def delete_room(self,room):
        uri=self._host+"/v1/rooms/"+str(room)
        self._request(self._requests.delete,uri,headers=self._headers())

    def list_room(self):
        uri=self._host+"/v1/rooms"
        r=self._request(self._requests.get,uri,headers=self._headers())
        return { item["name"]:item["_id"] for item in r.json() }

    def list_streams(self,room):
        uri=self._host+"/v1/rooms/"+str(room)+"/streams"
        r=self._request(self._requests.get,uri,headers=self._headers())
        return [item["id"] for item in r.json()]

    def delete_stream(self,room,stream):
        uri=self._host+"/v1/rooms/"+str(room)+"/streams/"+str(stream)
        self._request(self._requests.delete,uri,headers=self._headers())

    def list_participants(self,room):
        uri=self._host+"/v1/rooms/"+str(room)+"/participants"
        r=self._request(self._requests.get,uri,headers=self._headers())
        return len(r.json())

    def start_streaming_ins(self,room,rtsp_url,protocol="tcp"):
        options={
            "connection": {
                "url":str(rtsp_url),
                "transportProtocol": protocol,
                "bufferSize":212992,
            },
            "media": {
                "audio": "auto",
                "video":"auto"
            }
        }
        uri=self._host+"/v1/rooms/"+str(room)+"/streaming-ins"
        r=self._request(self._requests.post,uri,json=options,headers=self._headers())
        return r.json()["id"]

    def stop_streaming_ins(self,room,stream):
        uri=self._host+"/v1/rooms/"+str(room)+"/streaming-ins/"+str(stream)
        self._request(self._requests.delete,uri,headers=self._headers())

    def start_streaming_outs(self,room,url,video_from):
        media_options={
            "audio": False,
            "video": {
                "from": str(video_from)
            }
        }
        options={
            "protocol": "rtmp",
            "url": str(url),
            "media": media_options
        }
        print(options,flush=True)
        uri=self._host+"/v1/rooms/"+str(room)+"/streaming-outs"
        r=self._request(self._requests.post,uri,json=options,headers=self._headers())
        return r.json()

    def stop_streaming_outs(self,room,stream):
        uri=self._host+"/v1/rooms/"+str(room)+"/streaming-outs/"+str(stream)
        self._request(self._requests.delete,uri,headers=self._headers())

    def list_streaming_outs(self,room):
        uri=self._host+"/v1/rooms/"+str(room)+"/streaming-outs"
        r=self._request(self._requests.get,uri,headers=self._headers())
        return len(r.json())

    def create_token(self,room,user,role):
        uri=self._host+"/v1/rooms/"+str(room)+"/tokens"
        options={"user":user,"role":role}
        print(options, flush=True)
        r=self._request(self._requests.post,uri,json=options,headers=self._headers())
        print(r.text, flush=True)
        return r.text
