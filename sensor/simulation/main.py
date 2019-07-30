#!/usr/bin/python3

from db_ingest import DBIngest
from signal import signal, SIGTERM
import subprocess
import socket
import math
import time
import os
import re

def geo_point(origin, distance, tc):
    lat1=math.radians(origin[0])
    lon1=math.radians(origin[1])
    d=distance/111300.0
    lat = math.asin(math.sin(lat1)*math.cos(d)+math.cos(lat1)*math.sin(d)*math.cos(tc))
    dlon = math.atan2(math.sin(tc)*math.sin(d)*math.cos(lat1),math.cos(d)-math.sin(lat1)*math.sin(lat))
    lon=math.fmod(lon1-dlon+math.pi,2*math.pi)-math.pi
    return [math.degrees(lat), math.degrees(lon)]

office=list(map(float,os.environ["OFFICE"].split(",")))
resolution=list(map(int,os.environ["RESOLUTION"].split("x")))
dbhost=os.environ["DBHOST"]

pattern=str(os.environ["FILES"])
hostname=socket.gethostbyname(socket.gethostname())

theta = float(os.environ["THETA"])
mnth = float(os.environ["MNTH"])
alpha = float(os.environ["ALPHA"])
fovh = float(os.environ["FOVH"])
fovv = float(os.environ["FOVV"])

try:
    sensor_id=int(os.environ["SENSOR_ID"])
except:
    sensor_id=int(socket.gethostbyname(hostname).split(".")[3])

if "LOCATION" in os.environ:
    location=list(map(float,os.environ["LOCATION"].split(",")))
else:
    distance=float(os.environ["DISTANCE"])
    nsensors=int(os.environ["SENSORS"])
    angle=math.pi*2/nsensors*(sensor_id%nsensors)
    location=geo_point(office, distance, angle)
    theta=theta+angle/math.pi*180

db=None
r=None

def quit_service(signum, sigframe):
    try:
        if db and r: db.delete(r["_id"])
    except Exception as e:
        pass
    exit(143)

signal(SIGTERM, quit_service)
db=DBIngest(index="sensors",office=office,host=dbhost)
while True:
    try:
        r=db.ingest({
            "sensor": "camera",
            "icon": "camera.gif",
            "office": { "lat": office[0], "lon": office[1] },
            "model": "simulation",
            "resolution": { "width": resolution[0], "height": resolution[1] },
            "location": { "lat": location[0], "lon": location[1] },
            "url": "rtsp://"+hostname+":8554/live.sdp",
            "mac": "0098c00"+str(6963+sensor_id),
            'theta': theta,
            'mnth': mnth,
            'alpha': alpha,
            'fovh': fovh,
            'fovv': fovv,
            "status": "idle",
        })
        break
    except Exception as e:
        print("Exception: "+str(e), flush=True)
        time.sleep(10)

print("Created sensor "+r["_id"], flush=True)
while True:
    simulated_root="/mnt/simulated"
    files=[f for f in os.listdir(simulated_root) if re.search(pattern,f)]
    file1=simulated_root+"/"+files[sensor_id%len(files)]
    subprocess.call(["/usr/bin/cvlc","-vvv",file1,"--loop",":sout=#gather:rtp{sdp=rtsp://"+hostname+":8554/live.sdp}",":network-caching:1500",":sout-all",":sout-keep"],stdin=subprocess.DEVNULL,stderr=subprocess.DEVNULL)
    time.sleep(10)
