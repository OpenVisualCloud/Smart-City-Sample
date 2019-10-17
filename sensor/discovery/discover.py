#!/usr/bin/python3

from signal import SIGTERM, signal
from db_query import DBQuery
from db_ingest import DBIngest
from probe import probe, run
from onvif_discover import safe_discover
import time
import json
import os

port_scan=os.environ['PORT_SCAN']
sim_ports=list(map(int,os.environ["SIM_PORT"].strip("/").split("/"))) if "SIM_PORT" in os.environ else []
sim_prefix=os.environ["SIM_PREFIX"] if "SIM_PREFIX" in os.environ else ""
service_interval = float(os.environ["SERVICE_INTERVAL"]) if "SERVICE_INTERVAL" in os.environ else 30
office = list(map(float,os.environ["OFFICE"].split(","))) if "OFFICE" in os.environ else None
dbhost= os.environ["DBHOST"] if "DBHOST" in os.environ else None
sim_cameras={}

def probe_camera():
    command="/usr/bin/nmap "+port_scan+" -n"
    print(command, flush=True)
    for line in run(command.split(" ")):
        if line.startswith("Nmap scan report for"):
            ip=line.split(" ")[-1].strip("()")
        if "/tcp" in line and "open" in line:
            port=int(line.split("/")[0])
            yield ip,port

def probe_camera_info(ip, port, user='admin', passwd='admin'):
    desc=safe_discover(ip, port, user, passwd)
    if desc:
        rtspuri=desc["uri"][0]
        rtspuri=rtspuri.replace('rtsp://', "rtsp://"+user+":"+passwd+"@")
        camid=(None,None)
        if "device" in desc:
            return (rtspuri,("device.SerialNumber",desc['device']['SerialNumber']),desc)
        if "networks" in desc:
            return (rtspuri,("networks.HwAddress",desc['networks'][0]['HwAddress']),desc)

    if port in sim_ports:
        global sim_cameras
        rtspuri = "rtsp://"+ip+":"+str(port)+"/live.sdp"
        if rtspuri not in sim_cameras: sim_cameras[rtspuri]=len(sim_cameras.keys())
        camid=("simsn",sim_prefix+str(sim_cameras[rtspuri]))
        return (rtspuri,camid,{})

    return (None,None,None)

def quit_service(signum, sigframe):
    exit(143)

signal(SIGTERM, quit_service)

if dbhost:
    dbi=DBIngest(index="sensors",office=office,host=dbhost)
    dbs=DBQuery(index="sensors",office=office,host=dbhost)
    dbp=DBQuery(index="provisions",office=office,host=dbhost)

while True:
    for ip,port in probe_camera():
        print("Probing "+ip+":"+str(port), flush=True)
        try:
            rtspuri,camid,desc=probe_camera_info(ip,port)
            if rtspuri is None: continue
        except Exception as e:
            print("Exception: "+str(e), flush=True)
            continue
        #print(rtspuri, flush=True)
        #print(camid[0]+":"+camid[1], flush=True)

        # probe width & height from the stream
        width=height=0
        try:
            sinfo=probe(rtspuri)
            for stream in sinfo["streams"]:
                if "coded_width" in stream: width=int(stream["coded_width"])
                if "coded_height" in stream: height=int(stream["coded_height"])
        except Exception as e:
            print("Exception: "+str(e), flush=True)

        if width==0 or height==0:
            print("Unknown width & height, skipping", flush=True)
            continue
        sinfo["resolution"]={ "width": width, "height": height }
        sinfo.update(desc)
        sinfo.update({
            'sensor': 'camera',
            'model': 'ip_camera',
            'url': rtspuri,
            'status': 'idle',
        })
        print(json.dumps(sinfo,indent=2), flush=True) 

        if not dbhost: continue
        try:
            r=list(dbs.search("sensor:'camera' and "+camid[0]+"='"+camid[1]+"'",size=1))
            if not r:     # new camera
                print("Searching for template: "+camid[0]+"="+camid[1], flush=True)
                template=list(dbp.search(camid[0]+"='"+camid[1]+"'",size=1))
                if template:
                    print("Ingesting", flush=True)
                    record=template[0]["_source"]
                    record.update(sinfo)
                    dbi.ingest(record)
                else:
                    print("Template not found", flush=True)
            elif r[0]["_source"]["status"]=="disconnected":   # camera re-connect
                dbs.update(r[0]["_id"],sinfo)
        except Exception as e:
            print("Exception: "+str(e), flush=True)

    if not dbhost: break
    time.sleep(service_interval)
