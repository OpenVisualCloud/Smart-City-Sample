#!/usr/bin/python3

from ipaddress import IPv4Network
from threading import Thread
from queue import Queue
import socket
import select
import errno
import time
import re
import os

scan_nthreads=int(os.environ["SCAN_NTHREADS"]) if "SCAN_NTHREADS" in os.environ else 32
scan_batch=int(os.environ["SCAN_BATCH"]) if "SCAN_BATCH" in os.environ else 64
scan_timeout=float(os.environ["SCAN_TIMEOUT"]) if "SCAN_TIMEOUT" in os.environ else 200

class Scanner(object):
    def __init__(self, nthreads=scan_nthreads, batch=scan_batch, timeout=scan_timeout):
        super(Scanner, self).__init__()
        self._nthreads=nthreads
        self._batch=batch
        self._timeout=timeout

    def _parse_options(self, options):
        ports=[]
        networks=[]

        isport=False
        for arg1 in re.sub(" +"," ",options).split(" "):
            if arg1=="-p":
                isport=True
                continue

            if arg1.startswith("-p"):
                isport=True
                arg1=arg1[2:]

            if arg1.startswith("-"):
                print("Ignore unknown options: "+arg1, flush=True)
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

        return (networks, ports)
            
    def _scan_batch(self, iqueue, oqueue):
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
                oqueue.put(item)

        timebase=time.time()-self._timeout
        while True:
            timeout=time.time()-timebase
            if timeout<=0: break
            events = po.poll(timeout)
            if not events: break

            for e in events:
                item=items[e[0]]
                opt=item["s"].getsockopt(socket.SOL_SOCKET, socket.SO_ERROR)
                if opt==0: oqueue.put(item["item"])
                po.unregister(item["s"])

        for fileno in items:
            items[fileno]["s"].close()
                
    def _scan(self, iqueue, oqueue):
        queue=[]
        while True:
            item=iqueue.get()
            if not item: break
            
            queue.append(item)
            if len(queue)>self._batch:
                self._scan_batch(queue, oqueue)
                queue=[]

        if queue: self._scan_batch(queue, oqueue)
        oqueue.put(None)

    def _target(self, iqueue, options):
        networks,ports=self._parse_options(options)
        print("Scanning {}:{}".format(networks,ports), flush=True)

        for network1 in networks:
            for host1 in network1:
                print("Scanning {}".format(host1), flush=True)
                for port_range1 in ports:
                    for port1 in port_range1:
                        iqueue.put((host1.exploded, port1))

        for i in range(self._nthreads):
            iqueue.put(None)

    def scan(self, options):
        iqueue=Queue(self._nthreads*self._batch*2)
        oqueue=Queue()

        threads=[Thread(target=self._target,args=(iqueue,options))]
        threads.extend([Thread(target=self._scan,args=(iqueue,oqueue)) for i in range(self._nthreads)])
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
    for result in scanner.scan(sys.argv[1]):
        print(result, flush=True)
