#!/usr/bin/python3

from urllib.parse import unquote
from tornado import web,gen
from tornado.concurrent import run_on_executor
from concurrent.futures import ThreadPoolExecutor
from db_query import DBQuery
from language import text, encode
from configuration import env
import datetime
import socket

dbhost=env["DBHOST"]
proxyhost=env["PROXYHOST"]

db=DBQuery(index="offices",office="",host=dbhost)
offices={}

class RedirectHandler(web.RequestHandler):
    def __init__(self, app, request, **kwargs):
        super(RedirectHandler, self).__init__(app, request, **kwargs)
        self.executor= ThreadPoolExecutor(4)

    def check_origin(self, origin):
        return True

    @run_on_executor
    def _office_info(self, office):
        office_key=",".join(map(str,office))
        if office_key in offices:
            if (datetime.datetime.now()-offices[office_key]["time"]).total_seconds()<5*60:
                return offices[office_key]
        try:
            # search database for the office info
            r=list(db.search("location:["+office_key+"]",1))
            r[0]["time"]=datetime.datetime.now()
            offices[office_key]=r[0]
            return r[0]
        except Exception as e:
            print("Exception: "+str(e), flush=True)
            return text["connection error"]

    @gen.coroutine
    def get(self):
        office=unquote(self.get_argument("office",""))
        if office.find(",")>=0:
            r=yield self._office_info(list(map(float,office.split(","))))
        else:
            r={"_source":{"uri":proxyhost}}

        if isinstance(r, str):
            self.set_status(400, encode(r))
        else:
            uri=r["_source"]["uri"]+self.request.uri
            protocol=uri.split("://")[0]
            host=uri.split("/")[2]
            port=":"+host.split(":")[1] if uri.find(":")>=0 else ""
            host=socket.gethostbyname(host.partition(":")[0])
            path="/".join(uri.split("/")[3:])

            self.add_header('X-Accel-Redirect','/redirect/'+protocol+"/"+host+port+"/"+path)
            self.set_status(200,'OK')
