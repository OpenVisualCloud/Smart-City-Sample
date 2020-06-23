#!/usr/bin/python3

from signal import signal, SIGTERM
from concurrent.futures import ThreadPoolExecutor
import subprocess
import socket
import random
import time
import os
import re

simulated_root="/mnt/simulated"
files=[f for f in os.listdir(simulated_root) if re.search(os.environ["FILES"],f)]
rtsp_port=int(os.environ["RTSP_PORT"])
rtp_port=int(os.environ["RTP_PORT"])
port_step=int(os.environ["PORT_STEP"]) if "PORT_STEP" in os.environ else 100
ncameras=int(os.environ["NCAMERAS"])

def serve_stream(file1, rtsp_port1, rtp_port1):
    rtsp="rtsp://@:"+str(rtsp_port1)+"/live.sdp"
    while True:
        subprocess.call(["/usr/bin/cvlc","-vvv","--mtu=1200", file1,"--loop",":sout=#gather:rtp{sdp="+rtsp+",port="+str(rtp_port1)+"}",":network-caching:1500",":sout-all",":sout-keep"])
        time.sleep(10)

def quit_service(signum, sigframe):
    exit(143)

signal(SIGTERM, quit_service)
with ThreadPoolExecutor(ncameras) as e:
    for i in range(ncameras):
        e.submit(serve_stream, simulated_root+"/"+files[i%len(files)],rtsp_port+i*port_step,rtp_port+i*port_step)

