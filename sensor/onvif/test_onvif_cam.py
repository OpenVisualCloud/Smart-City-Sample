#!/usr/bin/python3

import sys
from onvif import ONVIFCamera, ONVIFError

def test_onvif_camera(ip, port, user, passwd):
    try:
        ONVIFCamera(ip, int(port), user, passwd, '/home/wsdl')
        print("Found onvif camera")
        sys.exit(0)
    except ONVIFError as e:
        #print("Failed to ceate Onvif Camera {}".format(e))
        sys.exit(1)

if __name__ == "__main__":
    if(len(sys.argv) != 5):
        print("Usage: " + sys.argv[0] + " ip-address port user password")
    else:
        test_onvif_camera(sys.argv[1], sys.argv[2], sys.argv[3], sys.argv[4])
