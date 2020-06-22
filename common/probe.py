#!/usr/bin/python3

from subprocess import Popen,PIPE,STDOUT

def run(cmd):
    with Popen(cmd,stdout=PIPE,stderr=STDOUT,bufsize=1,universal_newlines=True) as p:
        for line in p.stdout:
            yield line.strip()
        p.stdout.close()
        p.wait()

def probe(file1):
    print("Scanning "+file1)
    duration=0
    codec_type=None
    start_time= -1
    width=0
    height=0
    bandwidth=0

    for line in run(["/usr/local/bin/ffprobe","-v","error","-show_streams",file1]):
        i=line.find("=")
        if i<0: continue
        k=line[0:i]
        v=line[i+1:]
 
        # try parsing the value format
        if v=="N/A": continue
        if k=="codec_type": codec_type=v
        try:
            v=float(v)
            if codec_type=="video":
                if k=="coded_width": width=v
                if k=="coded_height": height=v
                if k=="duration" and v>duration: duration=v
                if k=="start_time" and (v<start_time or start_time<0): start_time=v
            if k=="bit_rate": bandwidth=bandwidth+v
        except:
            pass 

    return { 
        "duration": float(duration),
        "start_time": float(start_time),
        "resolution": {
            "width": int(width),
            "height": int(height),
        },
        "bandwidth": float(bandwidth),
    }

