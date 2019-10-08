#!/usr/bin/python3

from onvif import ONVIFCamera
import sys

# A fix for 'NotImplementedError: AnySimpleType.pytonvalue() not implemented'
# https://github.com/FalkTannhaeuser/python-onvif-zeep/issues/4
import zeep
def zeep_pythonvalue(self, xmlvalue):
    return xmlvalue
zeep.xsd.simple.AnySimpleType.pythonvalue = zeep_pythonvalue

def discover(ip, port):
    user = 'admin'
    passwd = 'admin'
    onvif_device_desc = {}
    cam = ONVIFCamera(ip, port, user, passwd, '/home/wsdl')

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

if __name__ == "__main__":
    if(len(sys.argv) >= 2):
        print("Usage: ip [port]")
        exit(-1)

    ip=sys.argv[1]
    port=int(sys.argv[2]) if len(sys.argv)>=3 else 554
    print(discover(ip, port), flush=True)

