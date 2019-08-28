#!/usr/bin/python3

from signal import signal, SIGTERM
import subprocess
import socket
import random
import time
import os
import re

simulated_root="/mnt/simulated"
files=[f for f in os.listdir(simulated_root) if re.search(os.environ["FILES"],f)]
sensor_id=int(os.environ["SENSOR_ID"]) if "SENSOR_ID" in os.environ else int(random.random()*len(files))
rtsphost=os.environ["RTSPHOST"] if "RTSPHOST" in os.environ else "rtsp://"+socket.gethostname()+":8554/live.sdp"

def quit_service(signum, sigframe):
    exit(143)

signal(SIGTERM, quit_service)
file1=simulated_root+"/"+files[sensor_id%len(files)]
while True:
    subprocess.call(["/usr/bin/cvlc","-vvv",file1,"--loop",":sout=#gather:rtp{sdp="+rtsphost+",proto=dccp}",":network-caching:1500",":sout-all",":sout-keep"])
    time.sleep(10)
