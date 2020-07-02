#!/usr/bin/python3

from signal import signal, SIGTERM
from concurrent.futures import ThreadPoolExecutor
from db_query import DBQuery
import subprocess
import socket
import random
import time
import os
import re

simulated_root="/mnt/simulated"
pattern=os.environ["FILES"]
rtsp_port=int(os.environ["RTSP_PORT"])
rtp_port=int(os.environ["RTP_PORT"])
port_step=int(os.environ["PORT_STEP"]) if "PORT_STEP" in os.environ else 100
ncameras=int(os.environ["NCAMERAS"])
algorithm=os.environ["ALGORITHM"]
dbhost=os.environ["DBHOST"] if "DBHOST" in os.environ else None
office=list(map(float,os.environ["OFFICE"].split(","))) if "OFFICE" in os.environ else None

def serve_stream(file1, rtsp_port1, rtp_port1):
    rtsp="rtsp://@:"+str(rtsp_port1)+"/live.sdp"
    while True:
        subprocess.call(["/usr/bin/cvlc","-vvv","--mtu=1200", file1,"--loop",":sout=#gather:rtp{sdp="+rtsp+",port="+str(rtp_port1)+"}",":network-caching:1500",":sout-all",":sout-keep"])
        time.sleep(10)

def quit_service(signum, sigframe):
    exit(143)

signal(SIGTERM, quit_service)

filters=[pattern for i in range(ncameras)]
if dbhost and office:
    db=DBQuery(index="provisions",office=office,host=dbhost)
    while True:
        try:
            for r1 in db.search("algorithm='{}' and office:[{},{}] and simfile:* and simsn:*".format(algorithm,office[0],office[1]),size=ncameras):
                m=re.search('[0-9]+$',r1["_source"]["simsn"])
                if not m: continue
                i=int(m.group(0))
                if i<ncameras: filters[i]=r1["_source"]["simfile"]
            break
        except:
            print("Waiting for DB...", flush=True)
            time.sleep(10)

files=list(os.listdir(simulated_root))
with ThreadPoolExecutor(ncameras) as e:
    for i in range(ncameras):
        file=[f for f in files if re.search(filters[i],f)]
        k=random.randint(0,len(file)-1)
        print("#{} camera: {}".format(i,file[k]),flush=True)
        e.submit(serve_stream, simulated_root+"/"+file[k],rtsp_port+i*port_step,rtp_port+i*port_step)

