#!/usr/bin/python3

from ipaddress import IPv4Network
from threading import Thread, Lock
from queue import Queue
from configuration import env
import socket
import select
import errno
import time
import re

scan_nthreads=int(env.get("SCAN_NTHREADS","32"))
scan_batch=int(env.get("SCAN_BATCH","64"))
scan_timeout=float(env.get("SCAN_TIMEOUT","200"))

class Scanner(object):
    def __init__(self, nthreads=scan_nthreads, batch=scan_batch, timeout=scan_timeout):
        super(Scanner, self).__init__()
        self._nthreads=nthreads
        self._batch=batch
        self._timeout=timeout
        self._hports=[80,443,554] # ports for host discovery
        self._lock=Lock()
        self._nhosts=0

    def _parse_options(self, options):
        ports=[]
        networks=[]

        isport=False
        flags=[]
        for arg1 in re.sub(" +"," ",options).split(" "):
            if arg1=="-p":
                isport=True
                continue

            if arg1.startswith("-p"):
                isport=True
                arg1=arg1[2:]

            if arg1.startswith("-"):
                flags.append(arg1)
                continue

            if isport:
                for port1 in arg1.split(","):
                    port1=list(map(int,port1.split(":")[-1].split("-")))
                    if len(port1)>2:
                        print("Ignore unknown port: "+port1, flush=True)
                        continue
                    if len(port1)<2: port1.append(port1[0])
                    ports.append(range(port1[0],port1[1]+1))
                isport=False
            elif arg1:
                try:
                    networks.append(IPv4Network(arg1))
                except:
                    try:
                        networks.append(IPv4Network(socket.gethostbyname(arg1)))
                    except:
                        print("Ignore invalid IP address: "+arg1, flush=True)

        return (networks, ports, flags)
            
    def _scan_batch(self, iqueue):
        items={}
        po = select.poll()
        for item in iqueue:
            s=socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            s.setblocking(0)
            s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

            try:
                items[s.fileno()]={ "s": s, "item": item }
                e=s.connect_ex(item)
            except Exception as e1:
                print("Exception {}".format(e1), flush=True)
                e=errno.EIO

            if e==errno.EINPROGRESS: 
                po.register(s)
            elif not e:
                yield item

        timebase=time.time()
        while time.time()-timebase<=self._timeout:
            events = po.poll(self._timeout)
            if not events: break

            for e in events:
                item=items[e[0]]
                opt=item["s"].getsockopt(socket.SOL_SOCKET, socket.SO_ERROR)
                if opt==0: yield item["item"]
                po.unregister(item["s"])

        for fileno in items:
            items[fileno]["s"].close()
                
    def _scan(self, iqueue, hqueue, oqueue):
        queue=[]
        while True:
            item=iqueue.get()
            if not item: break
            
            if not item[1]: # host scan
                for hp1 in self._scan_batch([(item[0],p1) for p1 in self._hports]):
                   hqueue.put(item[0])
                   break
                self._lock.acquire()
                self._nhosts=self._nhosts-1
                nhosts=self._nhosts
                self._lock.release()
                if nhosts<=0: hqueue.put(None)
            else: # port scan
                queue.append(item)
                if len(queue)>self._batch:
                    for hp1 in self._scan_batch(queue):
                        oqueue.put(hp1)
                    queue=[]

        if queue:
            for hp1 in self._scan_batch(queue):
                oqueue.put(hp1)

        oqueue.put(None)

    def _target(self, iqueue, hqueue, options):
        networks,ports,flags=self._parse_options(options)

        if "-Pn" in flags:
            for network1 in networks:
                for host1 in network1:
                    for port_range1 in ports:
                        for port1 in port_range1:
                            iqueue.put((host1.exploded, port1))
        else:
            for network1 in networks:
                for host1 in network1:
                    self._lock.acquire()
                    self._nhosts=self._nhosts+1
                    self._lock.release()
                    iqueue.put((host1.exploded, None))

            while True:
                host1=hqueue.get()
                if not host1: break
                for port_range1 in ports:
                    for port1 in port_range1:
                        iqueue.put((host1, port1))

        for i in range(self._nthreads):
            iqueue.put(None)

    def scan(self, options):
        iqueue=Queue(self._nthreads*self._batch*2)
        hqueue=Queue()
        oqueue=Queue()
        self._nhosts=0

        threads=[Thread(target=self._target,args=(iqueue,hqueue,options))]
        threads.extend([Thread(target=self._scan,args=(iqueue,hqueue,oqueue)) for i in range(self._nthreads)])
        for t in threads: t.start()

        i=0
        while i<self._nthreads:
            item=oqueue.get()
            if item: 
                yield item
            else:
                i=i+1
            
        for t in threads:
            t.join()
            
if __name__ == '__main__':
    import sys
    scanner=Scanner()
    for result in scanner.scan(" ".join(sys.argv[1:])):
        print(result, flush=True)
