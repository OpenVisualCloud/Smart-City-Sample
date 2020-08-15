#!/usr/bin/python3

from signal import SIGTERM, signal
from db_query import DBQuery
from db_ingest import DBIngest
from probe import probe
from onvif_discover import safe_discover
from scanner import Scanner
import traceback
import socket
import time
import json
import os

port_scan=[os.environ['PORT_SCAN']] if "PORT_SCAN" in os.environ else []
passcodes=os.environ['PASSCODE'].split(" ") if 'PASSCODE' in os.environ else []
sim_hosts=[hp.split(":") for hp in os.environ["SIM_HOST"].strip("/").split("/")] if "SIM_HOST" in os.environ else []
sim_prefix=os.environ["SIM_PREFIX"] if "SIM_PREFIX" in os.environ else ""
service_interval = float(os.environ["SERVICE_INTERVAL"]) if "SERVICE_INTERVAL" in os.environ else 30
office = list(map(float,os.environ["OFFICE"].split(","))) if "OFFICE" in os.environ else None
dbhost= os.environ["DBHOST"] if "DBHOST" in os.environ else None
sim_cameras={}

def quit_service(signum, sigframe):
    exit(143)

signal(SIGTERM, quit_service)

dbi=None
dbs=None
dbp=None
if dbhost and office:
    dbi=DBIngest(index="sensors",office=office,host=dbhost)
    dbs=DBQuery(index="sensors",office=office,host=dbhost)
    dbp=DBQuery(index="provisions",office=office,host=dbhost)
    dbp.wait()

def get_passcodes(ip, port):
    if office and dbhost:
        def _bucketize(query):
            r=dbp.bucketize(query,["passcode"])
            if "passcode" in r: 
                return [k for k in r["passcode"] if r["passcode"][k]]
            return []

        try:
            codes=_bucketize("passcode:* and ip={} and port={}".format(ip,port))
            if codes: return codes
            codes=_bucketize("passcode:* and ip={}".format(ip))
            if codes: return codes
            codes=_bucketize("passcode:*")
            if codes: return codes
        except:
            print(traceback.format_exc(), flush=True)
    return []
    
def probe_camera_info(ip, port):
    # check to see if ip/port is simulated
    for simh in sim_hosts:
        if str(port)!=simh[1]: continue
        if str(socket.gethostbyname(simh[0]))!=ip: continue

        global sim_cameras
        rtspuri = "rtsp://"+ip+":"+str(port)+"/live.sdp"
        if rtspuri not in sim_cameras: sim_cameras[rtspuri]=len(sim_cameras.keys())
        camid=("simsn",sim_prefix+str(sim_cameras[rtspuri]))
        return (rtspuri,[camid])

    if office and dbhost:
        r=list(dbp.search("ip={} and port={} and rtspurl:*".format(ip,port),size=1))
        if r:
            rtspuri=r[0]["_source"]["rtspurl"]
            return (rtspuri,[("rtspurl",rtspuri)])

    for passcode in get_passcodes(ip,port)+passcodes:
        print("OnVIF discovery over {}:{} {}".format(ip,port,passcode), flush=True)
        up=passcode.split(":")
        desc=safe_discover(ip, port, up[0], up[1])
        print(json.dumps(desc,indent=2), flush=True) 
        if desc:
            if "uri" in desc:
                rtspuri=desc["uri"][0].replace("rtsp://","rtsp://"+passcode+"@") if passcode!=":" else desc["uri"][0]
                camids=[]
                if "device" in desc:
                    if "SerialNumber" in desc['device']:
                        camids.append(("device.SerialNumber",desc['device']['SerialNumber']))
                if "networks" in desc:
                    for network1 in desc['networks']:
                        if "HwAddress" in network1:
                            camids.append(("networks.HwAddress",network1['HwAddress']))
                return (rtspuri,camids)

    return (None,[])

for simh in sim_hosts:
    if simh[1]=="0": continue
    port_scan.append("-p "+simh[1]+" "+simh[0])
print("port_scan={}".format(port_scan), flush=True)

scanner=Scanner()
while True:

    options=port_scan
    if dbp and not sim_hosts:
        r=dbp.bucketize("ip=* and port=*",["ip","port"])
        if r:
            options.extend([k for k in r["ip"] if r["ip"][k]])
            options.extend(["-p "+k for k in r["port"] if r["port"][k]])
        
    for ip,port in scanner.scan(" ".join(options)):
        # new or disconnected camera
        print("Probing "+ip+":"+str(port), flush=True)
        try:
            rtspuri,camids=probe_camera_info(ip,port)
            if rtspuri is None: continue
        except:
            print(traceback.format_exc(), flush=True)
            continue

        # check database to see if this camera is already registered
        r=None
        if dbhost:
            r=list(dbs.search("url='{}'".format(rtspuri),size=1))
            if r: 
                if r[0]["_source"]["status"]!="disconnected":
                    print("Skipping {}:{}:{}".format(ip,port,r[0]["_source"]["status"]),flush=True)
                    continue
            
        sinfo=probe(rtspuri)
        if sinfo["resolution"]["width"]==0 or sinfo["resolution"]["height"]==0:
            print("Unknown width & height, skipping", flush=True)
            continue

        sinfo.update({
            'sensor': 'camera',
            'model': 'ip_camera',
            'url': rtspuri,
            'status': 'idle',
        })

        if not dbhost: continue

        try:
            if not r: # new camera
                print("Searching for template", flush=True)
                template=list(dbp.search(" or ".join(['{}="{}"'.format(id1[0],id1[1]) for id1 in camids]),size=1))
                if not template: template=list(dbp.search("ip={} and port={}".format(ip,port),size=1))
                if template:
                    print("Ingesting", flush=True)
                    record=template[0]["_source"]
                    record.update(sinfo)
                    dbi.ingest(record)
                else:
                    print("Template not found", flush=True)
            else: # camera re-connect
                dbs.update(r[0]["_id"],sinfo)
        except Exception as e:
            print(traceback.format_exc(), flush=True)

    if not dbhost: break
    time.sleep(service_interval)
