#!/usr/bin/python3

import xml.etree.ElementTree as ET
from signal import SIGTERM, signal
from db_query import DBQuery
from db_ingest import DBIngest
from probe import probe
from onvif_discover import discover
from onvif_test import test
import subprocess
import sys
import time
import os

def parse_nmap_xml(nmapxml, sim_ports):
    root = ET.fromstring(nmapxml)
    for host1 in root.findall('host'):
        ip = host1.find("address").attrib['addr']
        ports = host1.find('ports')
        for port1 in ports.findall('port'):
            if(port1.attrib['protocol'] == 'tcp'):
                port = int(port1.attrib['portid'])

                print("To test " + ip + ":" + str(port), flush=True)
                if(test(ip, port) == True):
                    print("Found onvif device service", flush=True)
                    yield (ip,port)
                    continue

                print("Trying simulated camera", flush=True)
                if port in sim_ports:
                    for state1 in port1.findall('state'):
                        if state1.attrib['state'] == "open":
                            print("Found simulated camera", flush=True)
                            yield (ip,port)

def quit_service(signum, sigframe):
    exit(143)

signal(SIGTERM, quit_service)
ip_range = os.environ['IP_SCAN_RANGE']
port_range = os.environ['PORT_SCAN_RANGE']
sim_ports=list(map(int,os.environ["SIM_PORT"].strip("/").split("/")))
sim_prefix=os.environ["SIM_PREFIX"]
service_interval = float(os.environ["SERVICE_INTERVAL"])
office = list(map(float,os.environ["OFFICE"].split(",")))
dbhost= os.environ["DBHOST"]

dbi=DBIngest(index="sensors",office=office,host=dbhost)
dbs=DBQuery(index="sensors",office=office,host=dbhost)
dbp=DBQuery(index="provisions",office=office,host=dbhost)

sim_cameras={}
while True:
    xml=subprocess.check_output('/usr/bin/nmap -p'+port_range+' '+ip_range+' -Pn -oX -',stderr=subprocess.STDOUT,shell=True,timeout=100)
    
    for ip,port in parse_nmap_xml(xml, sim_ports):
        print("Start discovery "+ip+":"+str(port), flush=True)

        camid=None
        desc={}
        try:
            desc=discover(ip,port)
            camid=("MAC",desc["MAC"]) if "MAC" in desc else None
            if not camid:
                if "NetworkInterfaces" in desc:
                    if desc["NetworkInterfaces"]:
                        camid=("NetworkInterfaces.Info.HwAddress",desc['NetworkInterfaces'][0]['Info']['HwAddress'])
            if not camid:
                if "DeviceInformation" in desc:
                    camid=("DeviceInformation.SerialNumber",desc['DeviceInformation']['SerialNumber'])
        except Exception as e:
            print("Exception: "+str(e), flush=True)
            camid=None

        # Add credential to rtsp uri
        try:
            rtspuri = desc["MediaStreamUri"]["Uri"]
            rtspuri = rtspuri.replace('rtsp://', 'rtsp://admin:admin@')
        except:
            rtspuri = "rtsp://"+ip+":"+str(port)+"/live.sdp"
            index=sim_cameras[rtspuri] if rtspuri in sim_cameras else len(sim_cameras)
            camid=("simsn",sim_prefix+str(index))
        print("rtspuri: "+rtspuri, flush=True)

        # width & height
        sinfo={"streams":[]}
        try:
            width = int(desc["MediaVideoSources"][0]['Resolution']['Width'])
            height = int(desc["MediaVideoSources"][0]['Resolution']["Height"])
        except:
            # probe from the stream
            try:
                print("Probing for width & height", flush=True)
                sinfo=probe(rtspuri)
            except Exception as e:
                print("Exception: "+str(e), flush=True)

            width = 0
            height = 0
            for stream in sinfo["streams"]:
                if "coded_width" in stream: width=int(stream["coded_width"])
                if "coded_height" in stream: height=int(stream["coded_height"])
            if width==0 or height==0: 
                print("Unknown width & height, skipping", flush=True)
                continue

        try:
            found=list(dbs.search("sensor:'camera' and "+camid[0]+"='"+camid[1]+"'",size=1))
            if not found:
                template=list(dbp.search(camid[0]+"='"+camid[1]+"'",size=1))
                if template:
                    print("Ingesting", flush=True)
                    record=desc if desc else {}
                    record.update(template[0]["_source"])
                    record.update({
                        'sensor': 'camera',
                        'model': 'ip_camera',
                        'resolution': { 'width': width, 'height': height },
                        'url': rtspuri,
                        'status': 'idle',
                    })
                    dbi.ingest(record)

                    # register simulated cameras
                    if camid[0]=="simsn" and rtspuri not in cameras:
                        sim_cameras[rtspuri]=len(sim_cameras)
                else:
                    print("Template not found", flush=True)
        except Exception as e:
            print("Exception: "+str(e), flush=True)

    time.sleep(service_interval)
