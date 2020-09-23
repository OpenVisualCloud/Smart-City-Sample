#!/usr/bin/python3

from nginx import NGINX
from db_query import DBQuery
from threading import Event
from configuration import env
from socket import gethostbyname

dbhost=env["DBHOST"]

class NGINXRedirect(NGINX):
    def __init__(self, upstreams=[], stop=Event()):
        super(NGINXRedirect,self).__init__(upstreams, stop)
        self._db=DBQuery(index="offices",office="",host=dbhost)
        self._saved=self._upstreams

    def _update_upstreams(self):
        changed=super(NGINXRedirect,self)._update_upstreams()
        updates={ s:self._upstreams[s] for s in self._saved }
        try:
            for office1 in self._db.search("location:*",size=100):
                location=office1["_source"]["location"]
                name=("office"+str(location["lat"])+"c"+str(location["lon"])).replace("-","n").replace(".","d")
                protocol,q,host=office1["_source"]["uri"].partition("://")
                host,c,port=host.partition(":")

                if name in self._upstreams:
                    ip=self._upstreams[name][2]
                else:
                    changed=True
                    try:
                        ip=gethostbyname(host)
                    except:
                        ip="127.0.0.1"

                updates[name]=[host,c+port,ip]
        except:
            self._stop.wait(10)

        if not changed:
            for s in self._upstreams:
                if s not in updates:
                    changed=True
                    break

        self._upstreams=updates
        return changed

