#!/usr/bin/python3

from onvif import ONVIFCamera
import subprocess
import time
import sys

# A fix for 'NotImplementedError: AnySimpleType.pytonvalue() not implemented'
# https://github.com/FalkTannhaeuser/python-onvif-zeep/issues/4
import zeep
def zeep_pythonvalue(self, xmlvalue):
    return xmlvalue
zeep.xsd.simple.AnySimpleType.pythonvalue = zeep_pythonvalue

def _discover(ip, port, user, passwd):
    desc = {}

    try:
        cam = ONVIFCamera(ip, port, user, passwd, '/home/wsdl')
    except Exception as e:
        print("Exception: "+str(e), flush=True)
        return desc

    # Get Device Information
    # Scopes
    try:
        scopes = cam.devicemgmt.GetScopes()
        print("\n-------------- Scopes ------------------ ", flush=True)
        print(scopes, flush=True)
        scopelist = []
        for scope in scopes:
            scopelist.append(str(scope))
        desc['Scopes'] = scopelist
    except Exception as e:
        print("Failed to get scopes: "+str(e), flush=True)

    try:
        devInfo = cam.devicemgmt.GetDeviceInformation()
        print("\n---------- DeviceInformation ----------- ", flush=True)
        print(devInfo, flush=True)
        #desc['DeviceInformation'] = cam.devicemgmt.to_dict(devInfo)
        desc['DeviceInformation'] = devInfo
    except Exception as e:
        print("Failed to get device information: "+str(e), flush=True)

    # Get Services
    try:
        servList = cam.devicemgmt.GetServices(False)
        print("\n----------- Services -------------- ", flush=True)
        print(servList, flush=True)
        #desc['Services'] = cam.devicemgmt.to_dict(servList)
        desc['Services'] = servList
    except Exception as e:
        print("Failed to get services: "+str(e), flush=True)

    # Get Network Interfaces
    try:
        netIntfs = cam.devicemgmt.GetNetworkInterfaces()
        print("\n----------- NetworkInterfaces -------------- ", flush=True)
        print(netIntfs, flush=True)
        #desc['NetworkInterfaces'] = cam.devicemgmt.to_dict(netIntfs)
        desc['NetworkInterfaces'] = netIntfs
    except Exception as e:
        print("Failed to get network interfaces: "+str(e), flush=True)

    # Find all network protocols
    try:
        protocols = cam.devicemgmt.GetNetworkProtocols()
        print("\n-----------Protocols-------------- ", flush=True)
        print(protocols, flush=True)
        #desc['Protocols'] = cam.devicemgmt.to_dict(protocols)
        desc['Protocols'] = protocols
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
        #desc['MediaVideoSources'] = media_service.to_dict(videoSources)
        desc['MediaVideoSources'] = videoSources
    except Exception as e:
        print("Failed to get video sources: "+str(e), flush=True)

    # Video Source Configuration
    try:
        videoSourceCfgs = media_service.GetVideoSourceConfigurations()
        print("\n-----------Video Sources Cfg-------------- ", flush=True)
        print(videoSourceCfgs, flush=True)
        #desc['MediaVideoSourceConfiguration'] = media_service.to_dict(videoSourceCfgs)
        desc['MediaVideoSourceConfiguration'] = videoSourceCfgs
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
        #desc['MediaProfiles'] = media_service.to_dict(profiles)
        desc['MediaProfiles'] = profiles
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
        #desc['MediaStreamUri'] = media_service.to_dict(videoStrmUri)
        desc['MediaStreamUri'] = videoStrmUri
    except Exception as e:
        print("Failed to get media stream Uri: "+str(e), flush=True)
    return desc

def safe_discover(ip, port, user='admin', passwd='admin'):
    # timeout 2 seconds
    cnt = 0
    timeout = 2.0
    interval = 0.5
    is_timeout = False
    try:
        # this routine may hang. Put it into subprocess so we can timeout it.
        p = subprocess.Popen(["/home/onvif_discover.py", ip, str(port), user, passwd])
    except Exception as e:
        print("Excetion: "+str(e), flush=True)

    while p.poll() is None:
        if(cnt * interval > timeout ):
            is_timeout = True
            break
        time.sleep(interval)
        cnt += 1

    if(is_timeout == True):
        p.terminate()
        return None

    if(p.returncode == 0): 
        return _discover(ip, port, user, passwd)
    return None

if __name__ == "__main__":
    if(len(sys.argv) >= 2):
        print("Usage: ip [port [user [passwd]]]")
        exit(-1)

    ip=sys.argv[1]
    port=int(sys.argv[2]) if len(sys.argv)>=3 else 554
    user=sys.argv[3] if len(sys.argv)>=4 else "admin"
    passwd=sys.argv[4] if len(sys.argv)>=5 else "admin"
    print(_discover(ip, port, user, passwd), flush=True)
    exit(0)
