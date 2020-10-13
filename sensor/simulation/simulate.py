#!/usr/bin/python3

from signal import signal, SIGTERM
from concurrent.futures import ThreadPoolExecutor
from db_query import DBQuery
from configuration import env
import subprocess
import socket
import random
import time
import os
import re

simulated_root="/mnt/simulated"
pattern=env["FILES"]
rtsp_port=int(env["RTSP_PORT"])
rtp_port=int(env["RTP_PORT"])
port_step=int(env.get("PORT_STEP","100"))
ncameras=int(env["NCAMERAS"])
algorithm=env["ALGORITHM"]
dbhost=env.get("DBHOST",None)
office=list(map(float,env["OFFICE"].split(","))) if "OFFICE" in env else None

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
    db.wait()
    for r1 in db.search("algorithm='{}' and office:[{},{}] and simfile:* and simsn:*".format(algorithm,office[0],office[1]),size=ncameras):
        m=re.search('[0-9]+$',r1["_source"]["simsn"])
        if not m: continue
        i=int(m.group(0))
        if i<ncameras: filters[i]=r1["_source"]["simfile"]

files=list(os.listdir(simulated_root))
with ThreadPoolExecutor(ncameras) as e:
    k=random.randint(0,ncameras)
    for i in range(ncameras):
        files1=[f for f in files if re.search(filters[i],f)]
        file=files1[(i+k)%len(files1)]
        print("#{} camera: {}".format(i,file),flush=True)
        e.submit(serve_stream, simulated_root+"/"+file,rtsp_port+i*port_step,rtp_port+i*port_step)

