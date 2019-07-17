#!/usr/bin/python3
import os
import sys
import time
import json
import math
import urllib.parse
import subprocess
from onvif import ONVIFCamera, ONVIFError
import xml.etree.ElementTree as ET

from db_query import DBQuery
from db_ingest import DBIngest

# A fix for 'NotImplementedError: AnySimpleType.pytonvalue() not implemented'
# https://github.com/FalkTannhaeuser/python-onvif-zeep/issues/4
import zeep
def zeep_pythonvalue(self, xmlvalue):
    return xmlvalue
zeep.xsd.simple.AnySimpleType.pythonvalue = zeep_pythonvalue

def geo_point(origin, distance, tc):
    lat1=math.radians(origin[0])
    lon1=math.radians(origin[1])
    d=distance/111300.0
    lat = math.asin(math.sin(lat1)*math.cos(d)+math.cos(lat1)*math.sin(d)*math.cos(tc))
    dlon = math.atan2(math.sin(tc)*math.sin(d)*math.cos(lat1),math.cos(d)-math.sin(lat1)*math.sin(lat))
    lon=math.fmod(lon1-dlon+math.pi,2*math.pi)-math.pi
    return { "lat": math.degrees(lat), "lon": math.degrees(lon) }

def discover_onvif_camera(ip, port):

    user = 'admin'
    passwd = 'admin'
    onvif_device_desc = {}

    print('=========================== {}:{} ============================='.format(ip, port))

    onvif_device_desc['MAC'] = None

    print("\n-------------- Mac Address ------------------ ")

    try:
        cam = ONVIFCamera(ip, port, user, passwd, '/home/wsdl')
    except ONVIFError as e:
        print("Failed to ceate Onvif Camera {}".format(e))
        return

    # Get Device Information
    # Scopes
    try:
        scopes = cam.devicemgmt.GetScopes()
        print("\n-------------- Scopes ------------------ ")
        print(scopes)
        scopelist = []
        for scope in scopes:
            scopelist.append(str(scope))
        onvif_device_desc['Scopes'] = scopelist
    except ONVIFError as e:
        print("Failed to get scopes {}".format(e))
        pass

    try:
        devInfo = cam.devicemgmt.GetDeviceInformation()
        print("\n---------- DeviceInformation ----------- ")
        print(devInfo)
        #onvif_device_desc['DeviceInformation'] = cam.devicemgmt.to_dict(devInfo)
        onvif_device_desc['DeviceInformation'] = devInfo
    except ONVIFError as e:
        print("Failed to get device information {}".format(e))
        pass

    # Get Services
    try:
        servList = cam.devicemgmt.GetServices(False)
        print("\n----------- Services -------------- ")
        print(servList)
        #onvif_device_desc['Services'] = cam.devicemgmt.to_dict(servList)
        onvif_device_desc['Services'] = servList
    except ONVIFError as e:
        print("Failed to get services {}".format(e))
        pass

    # Get Network Interfaces
    try:
        netIntfs = cam.devicemgmt.GetNetworkInterfaces()
        print("\n----------- NetworkInterfaces -------------- ")
        print(netIntfs)
        #onvif_device_desc['NetworkInterfaces'] = cam.devicemgmt.to_dict(netIntfs)
        onvif_device_desc['NetworkInterfaces'] = netIntfs
    except ONVIFError as e:
        print("Failed to get network interfaces {}".format(e))
        pass

    # Find all network protocols
    try:
        protocols = cam.devicemgmt.GetNetworkProtocols()
        print("\n-----------Protocols-------------- ")
        print(protocols)
        #onvif_device_desc['Protocols'] = cam.devicemgmt.to_dict(protocols)
        onvif_device_desc['Protocols'] = protocols
    except ONVIFError as e:
        print("Failed to get network protocols {}".format(e))
        pass


    # Create MediaService
    try:
        media_service = cam.create_media_service()
    except ONVIFError as e:
        print("Failed to create media service {}".format(e))
        pass

    # Find video source
    try:
        videoSources = media_service.GetVideoSources()
        print("\n-----------Video Sources-------------- ")
        print(videoSources)
        #onvif_device_desc['MediaVideoSources'] = media_service.to_dict(videoSources)
        onvif_device_desc['MediaVideoSources'] = videoSources
    except ONVIFError as e:
        print("Failed to get video sources {}".format(e))
        pass


    # Video Source Configuration
    try:
        videoSourceCfgs = media_service.GetVideoSourceConfigurations()
        print("\n-----------Video Sources Cfg-------------- ")
        print(videoSourceCfgs)
        #onvif_device_desc['MediaVideoSourceConfiguration'] = media_service.to_dict(videoSourceCfgs)
        onvif_device_desc['MediaVideoSourceConfiguration'] = videoSourceCfgs
    except ONVIFError as e:
        print("Failed to get video sources configurations {}".format(e))
        pass

    # Find profiles
    profile_token = ''
    try:
        profiles = media_service.GetProfiles()
        print("\n-----------Media profiles-------------- ")
        #print(profiles)

        #for profile in profiles:
        #    profile['VideoEncoderConfiguration']['SessionTimeout'] = str(profile['VideoEncoderConfiguration']['SessionTimeout'])
        #    profile['PTZConfiguration']['DefaultPTZTimeout'] = str(profile['PTZConfiguration']['DefaultPTZTimeout'])

        profile_token = profiles[0].token
        #onvif_device_desc['MediaProfiles'] = media_service.to_dict(profiles)
        onvif_device_desc['MediaProfiles'] = profiles
    except ONVIFError as e:
        print("Failed to get media profiles {}".format(e))
        pass

    # Get Video Stream URI
    try:
        param = media_service.create_type('GetStreamUri')
        param.ProfileToken = profile_token
        param.StreamSetup = {'Stream': 'RTP-Unicast', 'Transport': {'Protocol': 'UDP'}}
        videoStrmUri = media_service.GetStreamUri(param)
        print("\n-----------Video Stream Uri-------------- ")
        print(videoStrmUri)
        videoStrmUri['Timeout'] = str(videoStrmUri['Timeout'])
        #onvif_device_desc['MediaStreamUri'] = media_service.to_dict(videoStrmUri)
        onvif_device_desc['MediaStreamUri'] = videoStrmUri
    except ONVIFError as e:
        print("Failed to get media stream Uri {}".format(e))
        pass

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
        proc = subprocess.Popen(['python3', cmd, ip, port, user, passwd])
    except Exception as e:
        print(e)    
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

def parse_nmap_xml(nmapxml, isfile):
    if(isfile):
        tree = ET.parse(nmapxml)
        root = tree.getroot()
    else:
        root = ET.fromstring(nmapxml)
    
    onvifcams = []
    for host in root.findall('host'):
        ip = host.find("address").attrib['addr']
        ports = host.find('ports')
        for port in ports.findall('port'):
            if(port.attrib['protocol'] == 'tcp'):
                    port = port.attrib['portid']
                    print("To test " + ip + ":" + port)
                    if(test_onvif_cam(ip, port) == True):                        
                        print("Found onvif device service")    
                        cam = {}
                        cam['ip'] = ip
                        cam['port'] = port
                        onvifcams.append(cam)
                    else:
                        print("Not onvif device service")    
    return onvifcams			           

def scan_onvif_camera(ip_range, port_range):
    onvifcams = []
    try:
        nmapxml = subprocess.check_output('nmap -p' + port_range + ' ' + ip_range + ' -oX -', stderr = subprocess.STDOUT, shell = True, timeout = 100)
        onvifcams = parse_nmap_xml(nmapxml, False)
    except:
        print('Failed to scan network')
    return onvifcams

def discover_all_onvif_cameras():
    
    ip_range = '192.168.1.0/24'
    port_range = '0-65535'

    if('IP_SCAN_RANGE' in os.environ):
        ip_range = os.environ['IP_SCAN_RANGE']

    if('PORT_SCAN_RANGE' in os.environ):
        port_range = os.environ['PORT_SCAN_RANGE']


    office = list(map(float,os.environ["OFFICE"].split(",")))
    distance = float(os.environ["DISTANCE"])
    angleoffset = float(os.environ["ANGLEOFFSET"])
    dbhost= os.environ["DBHOST"]

    sensor_index = 0
    mac_sensor_id = {}

    while True:
        desclist = []
        onvifcams = scan_onvif_camera(ip_range, port_range)
        nsensors = len(onvifcams)

        db = DBIngest(index="sensors",office=office,host=dbhost)
        dbs = DBQuery(index="sensors",office=office,host=dbhost)
        for cam in onvifcams:
            ip = cam['ip']
            port = int(cam['port'])
            desc = discover_onvif_camera(ip, port)

            if (desc['MAC'] == None):
                if('NetworkInterfaces' in desc):
                    if(len(desc['NetworkInterfaces']) >= 1):
                        desc['MAC'] = desc['NetworkInterfaces'][0]['Info']['HwAddress']

                # let's use camera serial number as id
                else:
                    desc['MAC'] = desc['DeviceInformation']['SerialNumber']

            if(desc['MAC'] not in mac_sensor_id):
                sensor_index += 1
                mac_sensor_id[desc['MAC']] = sensor_index
            sensor_id = mac_sensor_id[desc['MAC']]

            # Add credential to rtsp uri
            rtspuri = desc["MediaStreamUri"]["Uri"]
            rtspuri = rtspuri.replace('rtsp://', 'rtsp://admin:admin@')
            camdesc = {
                "sensor": "camera",
                "icon": "camera.gif",
                "office": { "lat": office[0], "lon": office[1] },
                "model": "ip_camera",
                "resolution": { "width": desc["MediaVideoSources"][0]['Resolution']['Width'], "height": desc["MediaVideoSources"][0]['Resolution']["Height"] },
                "location": geo_point(office, distance, math.pi * 2 / nsensors * sensor_id + math.pi * angleoffset / 180.0),
                "url": rtspuri,
                "mac": desc["MAC"],
                'theta': 15.0,
                'mnth': 15.0,
                'alpha': 45.0,
                'fovh': 90.0,
                'fovv': 68.0,
                "status": "idle",
            }

            print(camdesc)

            found = False
            try:
                for snr in dbs.search("sensor:'camera' and model:'ip_camera'"):
                    if (desc['MAC'] == snr['_source']['mac']):
                        found = True
            except Exception as e:
                print(e)

            if(found == False):
                desclist.append(camdesc)

        if(len(desclist) != 0):
            db.ingest_bulk(desclist)
        
        time.sleep(60)

if __name__ == "__main__":
    discover_all_onvif_cameras()
