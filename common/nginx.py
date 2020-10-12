#!/usr/bin/python3

from signal import SIGQUIT, SIGHUP
from subprocess import Popen
from threading import Thread, Event
import socket

class NGINX(object):
    def __init__(self, upstreams=[], stop=Event()):
        super(NGINX, self).__init__()
        self._stop=stop
        self._thread=None
        self._pid=None
        self._upstreams={}
        for s in upstreams:
            host,c,port=s[1].partition(":")
            self._upstreams[s[0]]=[host,c+port,"127.0.0.1"]

    def _update_upstreams(self):
        changed=False
        for s in self._upstreams:
            tmp=self._upstreams[s]
            try:
                ip=socket.gethostbyname(tmp[0])
            except:
                ip="127.0.0.1"
            if ip!=tmp[2]:
                tmp[2]=ip
                changed=True
        return changed

    def _monitor_ip_change(self):
        while not self._stop.is_set():
            if self._update_upstreams():
                print(self._upstreams, flush=True)
                with open("/etc/nginx/upstream.conf","wt") as fd:
                    for s in self._upstreams:
                        tmp=self._upstreams[s]
                        fd.write("upstream "+s+" { server "+tmp[2]+tmp[1]+"; }\n")

                if self._pid:
                    self._pid.send_signal(SIGHUP)

            if self._pid is None:
                self._pid=Popen(["/usr/local/sbin/nginx"])
            elif self._pid.poll() is not None:
                self._pid.wait()
                self._pid=None

            self._stop.wait(10)

    def start(self):
        self._thread=Thread(target=self._monitor_ip_change)
        self._thread.start()


    def stop(self):
        self._stop.set()
        if self._pid: 
            self._pid.send_signal(SIGQUIT)
        self.wait()

    def wait(self):
        if self._thread: 
            self._thread.join()
            self._thread=None

        if self._pid: 
            self._pid.wait()
            self._pid=None
