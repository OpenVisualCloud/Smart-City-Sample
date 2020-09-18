#!/usr/bin/python3

from subprocess import Popen, call
from threading import Thread, Event
import socket

class NGINX(object):
    def __init__(self, upstreams=[], stop=Event()):
        super(NGINX, self).__init__()
        self._nginx="/usr/local/sbin/nginx"
        self._stop=stop
        self._thread=None
        self._pid=None

        self._upstreams=[]
        for s in upstreams:
            hostport=s[1].split(":")
            self._upstreams.append([s[0],hostport[0],hostport[1],"127.0.0.1"])

    def _monitor_ip_change(self):
        while not self._stop.is_set():
            changed=False
            for s in self._upstreams:
                try:
                    ip=socket.gethostbyname(s[1])
                except:
                    ip="127.0.0.1"
                if ip!=s[3]:
                    s[3]=ip
                    changed=True

            if changed:
                with open("/etc/nginx/upstream.conf","wt") as fd:
                    for s in self._upstreams:
                        fd.write("upstream "+s[0]+" { server "+s[3]+":"+s[2]+"; }\n")
                call([self._nginx,"-s","reload"])

            self._stop.wait(5)

    def start(self):
        self._pid=Popen([self._nginx])
        if self._upstreams:
            self._thread=Thread(target=self._monitor_ip_change)
            self._thread.start()

    def stop(self):
        self._stop.set()

        if self._pid: 
            self._pid.send_signal(SIGQUIT)

        if self._thread: 
            self._thread.wait()
            self._thread=None

        if self._pid: 
            self._pid.wait()
            self._pid=None
