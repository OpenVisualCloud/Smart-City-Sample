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
    streams=[]
    sinfo={}
    for line in run(["/usr/bin/ffprobe","-v","error","-show_streams",file1]):
        if line=="[STREAM]": sinfo={}
        if line=="[/STREAM]": streams.append(sinfo)

        i=line.find("=")
        if i<0: continue
        keys=line[0:i].split(":")
        v=line[i+1:]
 
        # try parsing the value format
        if v=="N/A": continue
        if line[0:i]=="codec_type": codec_type=v
        if v == "true":
           v=True
        elif v == "false":
           v=False
        else:
            try:
                v=int(v)
            except:
                try:
                    v=float(v)
                    # calculate the stream duration
                    if codec_type=="video":
                        if line[0:i]=="duration" and v>duration: duration=v
                        if line[0:i]=="start_time" and (v<start_time or start_time<0): start_time=v
                except:
                    pass 

        # set k:v
        s1=sinfo
        for k in keys[:-1]:
            if k not in s1: s1[k]={}
            s1=s1[k]
        s1[keys[-1]]=v

    return { "duration": duration, "start_time": start_time, "streams": streams }
