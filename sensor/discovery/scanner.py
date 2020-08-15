#!/usr/bin/python3

from ipaddress import IPv4Network
from threading import Thread
from queue import Queue
import socket
import re

class Scanner(object):
    def __init__(self):
        super(Scanner, self).__init__()
        self._batch_size=32

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
            
    def _scan(self, iqueue, oqueue):
        while True:
            item=iqueue.get()
            if not item: break
            
            s=socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
            s.settimeout(0.2)

            try:
                if not s.connect_ex(item):
                    oqueue.put(item)
            except Exception as e:
                print(e, flush=True)

            s.close()
        oqueue.put(None)

    def _target(self, iqueue, options):
        networks,ports=self._parse_options(options)
        print("Scanning {}:{}".format(networks,ports), flush=True)

        for network1 in networks:
            for host1 in network1:
                for port_range1 in ports:
                    for port1 in port_range1:
                        iqueue.put((host1.exploded, port1))

        for i in range(self._batch_size):
            iqueue.put(None)

    def scan(self, options):
        iqueue=Queue(self._batch_size)
        oqueue=Queue()

        threads=[Thread(target=self._target,args=(iqueue,options))]
        threads.extend([Thread(target=self._scan,args=(iqueue,oqueue)) for i in range(self._batch_size)])
        for t in threads: t.start()

        i=0
        while i<self._batch_size:
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
