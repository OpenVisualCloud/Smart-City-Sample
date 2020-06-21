#!/usr/bin/python3

from onvif import ONVIFCamera
import subprocess
import time
import sys
import os

no_proxy=os.environ["no_proxy"].split(",") if "no_proxy" in os.environ else []

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

        #try:
        #    scopes = cam.devicemgmt.GetScopes()
        #    desc['scopes']=[str(x) for x in scopes]
        #except Exception as e:
        #    print("GetScopes Exception: "+str(e), flush=True)

        try:
            device = cam.devicemgmt.GetDeviceInformation()
            desc['device']=cam.devicemgmt.to_dict(device)
        except Exception as e:
            print("GetDeviceInfo Exception: "+str(e), flush=True)

        #try:
        #    services = cam.devicemgmt.GetServices(False)
        #    desc['services']=cam.devicemgmt.to_dict(services)
        #except Exception as e:
        #    print("GetServices Exception: "+str(e), flush=True)

        try:
            networks = cam.devicemgmt.GetNetworkInterfaces()
            desc['networks']=[x["Info"] for x in cam.devicemgmt.to_dict(networks)]
        except Exception as e:
            print("GetNetworks Exception: "+str(e), flush=True)

        #try:
        #    protocols = cam.devicemgmt.GetNetworkProtocols()
        #    desc['protocols']=cam.devicemgmt.to_dict(protocols)
        #except Exception as e:
        #    print("GetProtocols Exception: "+str(e), flush=True)

        try:
            media_service = cam.create_media_service()

            try:
                profiles = media_service.GetProfiles()
                profile_token = profiles[0].token
                #desc['profiles'] = media_service.to_dict(profiles)

                desc['uri']=[]
                for p1 in profiles:
                    try:
                        t1=media_service.create_type('GetStreamUri')
                        t1.ProfileToken = p1.token
                        t1.StreamSetup={
                            'Stream':'RTP-Unicast',
                            'Transport':{
                                'Protocol': 'UDP',
                            },
                        }
                        uri=media_service.GetStreamUri(t1)
                        desc['uri'].append(media_service.to_dict(uri)["Uri"])
                    except Exception as e:
                        print("GetStreamUri Exception: "+str(e), flush=True)

            except Exception as e:
                print("GetProfiles Exception: "+str(e), flush=True)

            #desc['video']={}
            #try:
            #    videos = media_service.GetVideoSources()
            #    desc['video']['sources']=media_service.to_dict(videos)
            #except Exception as e:
            #    print("GetVideos Exception: "+str(e), flush=True)

            #try:
            #    configs = media_service.GetVideoSourceConfigurations()
            #    desc['video']['configs']=media_service.to_dict(configs)
            #except Exception as e:
            #    print("GetVideoConfigs Exception: "+str(e), flush=True)

        except Exception as e:
            print("MediaService Exception: "+str(e), flush=True)

    except Exception as e:
        print("OnVIFCamera Exception: "+str(e), flush=True)

    return desc

def safe_discover(ip, port, user, passwd):
    # timeout 2 seconds
    cnt = 0
    timeout = 2.0
    interval = 0.5
    is_timeout = False
    
    # put IP into no_proxy environment variable
    os.environ["no_proxy"]=",".join(no_proxy+[str(ip)])
    
    # this routine may hang. Put it into subprocess so we can timeout it.
    p = subprocess.Popen(["/home/onvif_discover.py", ip, str(port), user, passwd], stdout=subprocess.DEVNULL,stderr=subprocess.DEVNULL)
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
    if(len(sys.argv) < 5):
        print("Usage: ip port user passwd")
        exit(-1)
    _discover(sys.argv[1], int(sys.argv[2]), sys.argv[3], sys.argv[4])
    exit(0)
