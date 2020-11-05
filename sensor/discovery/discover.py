#!/usr/bin/python3

from signal import SIGTERM, signal
from db_query import DBQuery
from db_ingest import DBIngest
from probe import probe
from onvif_discover import safe_discover
from scanner import Scanner
from streamer import Streamer
from configuration import env
import traceback
import socket
import time
import json

port_scan=[env['PORT_SCAN']] if "PORT_SCAN" in env else []
passcodes=env['PASSCODE'].split(" ") if 'PASSCODE' in env else []
sim_hosts=[hp.split(":") for hp in env["SIM_HOST"].strip("/").split("/")] if "SIM_HOST" in env else []
sim_prefix=env.get("SIM_PREFIX","")
service_interval = float(env.get("SERVICE_INTERVAL","30"))
office = list(map(float,env["OFFICE"].split(","))) if "OFFICE" in env else None
dbhost= env.get("DBHOST",None)
camera_gateway = env["CAMERA_GATEWAY_ENABLE"]
rtmp_host= env.get("RTMP_HOST",None)
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
            r=dbp.bucketize(query,["passcode"], size=1000)
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
        try:
            if str(socket.gethostbyname(simh[0]))!=ip: continue
        except:
            continue

        global sim_cameras
        rtspuri = "rtsp://"+ip+":"+str(port)+"/live.sdp"
        if rtspuri not in sim_cameras: sim_cameras[rtspuri]=len(sim_cameras.keys())
        camid=("simsn",sim_prefix+str(sim_cameras[rtspuri]))
        return (rtspuri,[camid],{"manufacturer":"Simulated","serial":camid[1]},True)

    if office and dbhost:
        r=list(dbp.search("ip={} and port={} and rtspurl:*".format(ip,port),size=1))
        if r:
            rtspuri=r[0]["_source"]["rtspurl"]
            dinfo={ k:r[0]["_source"][k] for k in ["manufacturer","model","serial"] if k in r[0]["_source"] }
            return (rtspuri,[("rtspurl",rtspuri)],dinfo,False)

    for passcode in get_passcodes(ip,port)+passcodes:
        print("OnVIF discovery over {}:{} {}".format(ip,port,passcode), flush=True)
        up=passcode.split(":")
        desc=safe_discover(ip, port, up[0], up[1])
        print(json.dumps(desc,indent=2), flush=True) 
        if desc:
            if "uri" in desc:
                rtspuri=desc["uri"][0].replace("rtsp://","rtsp://"+passcode+"@") if passcode!=":" else desc["uri"][0]
                camids=[]
                dinfo={}
                if "device" in desc:
                    if "SerialNumber" in desc['device']:
                        camids.append(("device.SerialNumber",desc['device']['SerialNumber']))
                    if "Manufacturer" in desc['device']:
                        dinfo["manufacturer"]=desc['device']['Manufacturer']
                    if "Model" in desc['device']:
                        dinfo["model"]=desc['device']['Model']
                    if "SerialNumber" in desc['device']:
                        dinfo["serial"]=desc['device']['SerialNumber']
                if "networks" in desc:
                    for network1 in desc['networks']:
                        if "HwAddress" in network1:
                            camids.append(("networks.HwAddress",network1['HwAddress']))
                return (rtspuri,camids,dinfo,False)

    return (None,[],{},Flase)

for simh in sim_hosts:
    if simh[1]=="0": continue
    port_scan.append("-p "+simh[1]+" "+simh[0])

scanner=Scanner()
streamer=None
if camera_gateway=="enable": streamer=Streamer()
while True:

    options=port_scan
    if dbp and not sim_hosts:
        try:
            r=dbp.bucketize("ip_text:* or port:*",["ip_text","port"],size=1000)
            if r:
                options.extend([k for k in r["ip_text"] if r["ip_text"][k]])
                options.extend(["-p "+str(k) for k in r["port"] if r["port"][k]])
        except:
            print(traceback.format_exc(), flush=True)
            continue
        
    for ip,port in scanner.scan(" ".join(options)):
        # new or disconnected camera
        print("Probing "+ip+":"+str(port), flush=True)
        try:
            rtspuri,camids,dinfo,simulation=probe_camera_info(ip,port)
            if rtspuri is None: continue
        except:
            print(traceback.format_exc(), flush=True)
            continue

        # check database to see if this camera is already registered
        r=None
        if dbhost:
            r=list(dbs.search("url='{}'".format(rtspuri),size=1))
            try:
                if camera_gateway=="enable":
                    r=list(dbs.search("rtspuri='{}'".format(rtspuri),size=1))
                else:
                    r=list(dbs.search("url='{}'".format(rtspuri),size=1))
                if r:
                    if r[0]["_source"]["status"]!="disconnected":
                        print("Skipping {}:{}:{}".format(ip,port,r[0]["_source"]["status"]),flush=True)
                        continue
            except:
                print(traceback.format_exc(), flush=True)
                continue
            
        sinfo=probe(rtspuri)
        if sinfo["resolution"]["width"]==0 or sinfo["resolution"]["height"]==0:
            print("Unknown width & height, skipping", flush=True)
            continue

        sinfo.update(dinfo)
        if camera_gateway=="disable":
            sinfo.update({
                'type': 'camera',
                'subtype': 'ip_camera',
                'rtspuri': rtspuri,
                'url': rtspuri,
                'status': 'idle',
            })
        else:
            sinfo.update({
                'type': 'camera',
                'subtype': 'ip_camera',
                'rtspuri': rtspuri,
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
                    record.pop('passcode',None)
                    dbi.ingest(record,refresh="wait_for")
                    # query the sensor id with rtspuri
                    if camera_gateway=="enable":
                        r=list(dbs.search("rtspuri='{}'".format(rtspuri),size=1))
                        if r:
                            sensor=r[0]["_id"]
                            rtmpuri=rtmp_host+"/"+str(sensor)
                            # rtsp -> rtmp
                            streamer.set(sensor,rtspuri,rtmpuri,simulation)
                            # update the url
                            sinfo.update({"url":rtmpuri})
                            dbs.update(sensor,sinfo)
                else:
                    print("Template not found", flush=True)
            else: # camera re-connect
                if camera_gateway=="enable":
                    sinfo.update({"url":r[0]["_source"]["url"]})
                dbs.update(r[0]["_id"],sinfo)
        except Exception as e:
            print(traceback.format_exc(), flush=True)
            continue

    if not dbhost: break
    time.sleep(service_interval)
