#!/usr/bin/python3

from onvif import ONVIFCamera
import subprocess
import sys
import time

def test(ip, port):
    user = 'admin'
    passwd = 'admin'
    # timeout 2 seconds
    cnt = 0
    timeout = 2.0
    interval = 0.5
    is_timeout = False
    try:
        # this routine may hang. Put it into subprocess so we can timeout it.
        proc = subprocess.Popen(["/home/onvif_test.py", ip, str(port), user, passwd])
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

    if(proc.returncode == 0): return True
    return False

if __name__ == "__main__":
    if(len(sys.argv) != 5):
        print("Usage: ip-address port user password")
        exit(-1)

    try:
        ONVIFCamera(sys.argv[1], int(sys.argv[2]), sys.argv[3], sys.argv[4], '/home/wsdl')
        print("Found onvif camera")
        exit(0)
    except Exception as e:
        print("Exception: "+str(e))
        exit(1)
