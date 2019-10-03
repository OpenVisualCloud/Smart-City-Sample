#!/usr/bin/python3
import os
import sys
import time
import subprocess
from onvif import ONVIFCamera
import xml.etree.ElementTree as ET
from signal import SIGTERM, signal

from db_query import DBQuery
from db_ingest import DBIngest
from probe import probe

# A fix for 'NotImplementedError: AnySimpleType.pytonvalue() not implemented'
# https://github.com/FalkTannhaeuser/python-onvif-zeep/issues/4
import zeep
def zeep_pythonvalue(self, xmlvalue):
    return xmlvalue
zeep.xsd.simple.AnySimpleType.pythonvalue = zeep_pythonvalue

def discover_onvif_camera(ip, port):
    user = 'admin'
    passwd = 'admin'
    onvif_device_desc = {}

    print('=========================== {}:{} ============================='.format(ip, port), flush=True)

    onvif_device_desc['MAC'] = None

    print("\n-------------- Mac Address ------------------ ", flush=True)

    try:
        cam = ONVIFCamera(ip, port, user, passwd, '/home/wsdl')
    except Exception as e:
        print("Failed to create an ONVIF camera: "+str(e), flush=True)
        return onvif_device_desc

    # Get Device Information
    # Scopes
    try:
        scopes = cam.devicemgmt.GetScopes()
        print("\n-------------- Scopes ------------------ ", flush=True)
        print(scopes, flush=True)
        scopelist = []
        for scope in scopes:
            scopelist.append(str(scope))
        onvif_device_desc['Scopes'] = scopelist
    except Exception as e:
        print("Failed to get scopes: "+str(e), flush=True)

    try:
        devInfo = cam.devicemgmt.GetDeviceInformation()
        print("\n---------- DeviceInformation ----------- ", flush=True)
        print(devInfo, flush=True)
        #onvif_device_desc['DeviceInformation'] = cam.devicemgmt.to_dict(devInfo)
        onvif_device_desc['DeviceInformation'] = devInfo
    except Exception as e:
        print("Failed to get device information: "+str(e), flush=True)

    # Get Services
    try:
        servList = cam.devicemgmt.GetServices(False)
        print("\n----------- Services -------------- ", flush=True)
        print(servList, flush=True)
        #onvif_device_desc['Services'] = cam.devicemgmt.to_dict(servList)
        onvif_device_desc['Services'] = servList
    except Exception as e:
        print("Failed to get services: "+str(e), flush=True)

    # Get Network Interfaces
    try:
        netIntfs = cam.devicemgmt.GetNetworkInterfaces()
        print("\n----------- NetworkInterfaces -------------- ", flush=True)
        print(netIntfs, flush=True)
        #onvif_device_desc['NetworkInterfaces'] = cam.devicemgmt.to_dict(netIntfs)
        onvif_device_desc['NetworkInterfaces'] = netIntfs
    except Exception as e:
        print("Failed to get network interfaces: "+str(e), flush=True)

    # Find all network protocols
    try:
        protocols = cam.devicemgmt.GetNetworkProtocols()
        print("\n-----------Protocols-------------- ", flush=True)
        print(protocols, flush=True)
        #onvif_device_desc['Protocols'] = cam.devicemgmt.to_dict(protocols)
        onvif_device_desc['Protocols'] = protocols
    except Exception as e:
        print("Failed to get network protocols: "+str(e), flush=True)

    # Create MediaService
    try:
        media_service = cam.create_media_service()
    except Exception as e:
        print("Failed to create media service: "+str(e), flush=True)

    # Find video source
    try:
        videoSources = media_service.GetVideoSources()
        print("\n-----------Video Sources-------------- ", flush=True)
        print(videoSources, flush=True)
        #onvif_device_desc['MediaVideoSources'] = media_service.to_dict(videoSources)
        onvif_device_desc['MediaVideoSources'] = videoSources
    except Exception as e:
        print("Failed to get video sources: "+str(e), flush=True)

    # Video Source Configuration
    try:
        videoSourceCfgs = media_service.GetVideoSourceConfigurations()
        print("\n-----------Video Sources Cfg-------------- ", flush=True)
        print(videoSourceCfgs, flush=True)
        #onvif_device_desc['MediaVideoSourceConfiguration'] = media_service.to_dict(videoSourceCfgs)
        onvif_device_desc['MediaVideoSourceConfiguration'] = videoSourceCfgs
    except Exception as e:
        print("Failed to get video sources configurations: "+str(e), flush=True)

    # Find profiles
    profile_token = ''
    try:
        profiles = media_service.GetProfiles()
        print("\n-----------Media profiles-------------- ", flush=True)
        #print(profiles)

        #for profile in profiles:
        #    profile['VideoEncoderConfiguration']['SessionTimeout'] = str(profile['VideoEncoderConfiguration']['SessionTimeout'])
        #    profile['PTZConfiguration']['DefaultPTZTimeout'] = str(profile['PTZConfiguration']['DefaultPTZTimeout'])

        profile_token = profiles[0].token
        #onvif_device_desc['MediaProfiles'] = media_service.to_dict(profiles)
        onvif_device_desc['MediaProfiles'] = profiles
    except Exception as e:
        print("Failed to get media profiles: "+str(e), flush=True)

    # Get Video Stream URI
    try:
        param = media_service.create_type('GetStreamUri')
        param.ProfileToken = profile_token
        param.StreamSetup = {'Stream': 'RTP-Unicast', 'Transport': {'Protocol': 'UDP'}}
        videoStrmUri = media_service.GetStreamUri(param)
        print("\n-----------Video Stream Uri-------------- ", flush=True)
        print(videoStrmUri, flush=True)
        videoStrmUri['Timeout'] = str(videoStrmUri['Timeout'])
        #onvif_device_desc['MediaStreamUri'] = media_service.to_dict(videoStrmUri)
        onvif_device_desc['MediaStreamUri'] = videoStrmUri
    except Exception as e:
        print("Failed to get media stream Uri: "+str(e), flush=True)

    return onvif_device_desc

def test_onvif_cam(ip, port):
    cmd = 'test_onvif_cam.py'
    user = 'admin'
    passwd = 'admin'
    # timeout 2 seconds
    cnt = 0
    timeout = 2.0
    interval = 0.5
    is_timeout = False
    try:
        proc = subprocess.Popen(['python3', cmd, ip, str(port), user, passwd])
    except Exception as e:
        print(e, flush=True)    
    while proc.poll() is None:
        if(cnt * interval > timeout ):
            is_timeout = True
            break
        time.sleep(interval)
        cnt += 1

    if(is_timeout == True):
        proc.terminate()
        return False

    if(proc.returncode == 0):    
        return True
    return False         

def parse_nmap_xml(nmapxml, simulated):
    onvifcams = []
    root = ET.fromstring(nmapxml)
    for host1 in root.findall('host'):
        ip = host1.find("address").attrib['addr']
        ports = host1.find('ports')
        for port1 in ports.findall('port'):
            if(port1.attrib['protocol'] == 'tcp'):
                port = int(port1.attrib['portid'])

                print("To test " + ip + ":" + str(port), flush=True)
                if(test_onvif_cam(ip, port) == True):                        
                    print("Found onvif device service", flush=True)    
                    onvifcams.append((ip,port))
                    continue

                print("Trying simulated camera", flush=True)
                if port in simulated:
                    for state1 in port1.findall('state'):
                        if state1.attrib['state'] == "open":
                            print("Found simulated camera", flush=True)
                            onvifcams.append((ip,port))
    return onvifcams

def quit_service(signum, sigframe):
    exit(143)

signal(SIGTERM, quit_service)
ip_range = os.environ['IP_SCAN_RANGE']
port_range = os.environ['PORT_SCAN_RANGE']
simulated=list(map(int,os.environ["SIMULATED_CAMERA"].strip("/").split("/")))
locations = [list(map(float,loc.split(","))) for loc in os.environ['LOCATION'].strip('/').split('/')]
addresses = os.environ['ADDRESS'].strip('/').split("/")
thetas = [float(theta) for theta in os.environ['THETA'].strip('/').split('/')]
service_interval = float(os.environ["SERVICE_INTERVAL"])
office = list(map(float,os.environ["OFFICE"].split(",")))
dbhost= os.environ["DBHOST"]

db = DBIngest(index="sensors",office=office,host=dbhost)
dbs = DBQuery(index="sensors",office=office,host=dbhost)
cameras={}
while True:
    xml=subprocess.check_output('/usr/bin/nmap -p'+port_range+' '+ip_range+' -Pn -oX -',stderr=subprocess.STDOUT,shell=True,timeout=100)

    for ip,port in parse_nmap_xml(xml, simulated):
        print("Start discovery "+ip+":"+str(port), flush=True)
        desc = discover_onvif_camera(ip, port)

        try:
            if (desc['MAC'] == None):
                if('NetworkInterfaces' in desc):
                    if(len(desc['NetworkInterfaces']) >= 1):
                        desc['MAC'] = desc['NetworkInterfaces'][0]['Info']['HwAddress']

                # let's use camera serial number as id
                else:
                    desc['MAC'] = desc['DeviceInformation']['SerialNumber']
            mac=desc['MAC']
        except:
            mac="567890"+('7'.join(ip.split(".")))+"9"+str(port)
        print("mac: "+mac, flush=True)

        # Add credential to rtsp uri
        try:
            rtspuri = desc["MediaStreamUri"]["Uri"]
            rtspuri = rtspuri.replace('rtsp://', 'rtsp://admin:admin@')
        except:
            rtspuri = "rtsp://"+ip+":"+str(port)+"/live.sdp"
        print("rtspuri: "+rtspuri, flush=True)

        # width & height
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
                sinfo={"streams":[]}

            width = 0
            height = 0
            for stream in sinfo["streams"]:
                if "coded_width" in stream: width=int(stream["coded_width"])
                if "coded_height" in stream: height=int(stream["coded_height"])
            if width==0 or height==0: 
                print("Unknown width & height, skipping", flush=True)
                continue

        # retrieve unique location
        if mac not in cameras: cameras[mac]=len(cameras.keys())
        try:
            print("Checking for preexistance", flush=True)
            found=list(dbs.search("sensor:'camera' and model:'ip_camera' and mac='"+mac+"'", size=1))
            if not found:
                print("Ingesting", flush=True)
                location = locations[int(cameras[mac]%len(locations))]
                db.ingest({
                    'sensor': 'camera',
                    'office': { 'lat': office[0], 'lon': office[1] },
                    'model': 'ip_camera',
                    'resolution': { 'width': width, 'height': height },
                    'location': { "lat": location[0], "lon": location[1] },
                    'address': addresses[int(cameras[mac]%len(addresses))],
                    'url': rtspuri,
                    'mac': mac,
                    'theta': thetas[int(cameras[mac]%len(thetas))],
                    'mnth': 75.0,
                    'alpha': 45.0,
                    'fovh': 90.0,
                    'fovv': 68.0,
                    'status': 'idle',
                })
        except Exception as e:
            print("Exception: "+str(e), flush=True)

    time.sleep(service_interval)
