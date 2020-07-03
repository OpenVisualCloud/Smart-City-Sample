#!/usr/bin/python3

from db_ingest import DBIngest
import os
import json

dbhost=os.environ["DBHOST"]
office=list(map(float,os.environ["OFFICE"].split(",")))
officestr='$'.join(map(str,office))
proxyhost=os.environ["PROXYHOST"]
scenario=os.environ["SCENARIO"]
zone=os.environ["ZONE"]

print("Provisioning...", flush=True)

# populate db with simulated offices and provisionings
with open("/run/secrets/sensor-info.json",encoding='utf-8') as fd:
    data=json.load(fd)
    dbo=DBIngest(index="offices",office="",host=dbhost)
    dbp=DBIngest(index="provisions", office=office, host=dbhost)
    for office1 in data:
        if scenario != office1["scenario"]: continue
        location1=office1["location"]
        if location1["lat"]!=office[0] or location1["lon"]!=office[1]: continue
        office1.pop("scenario")

        sensors=office1.pop("sensors")
        office1["uri"]=proxyhost
        office1["zone"]=zone
        dbo.ingest(office1,officestr)

        for s in sensors: 
            s["office"]=location1
            if "ip" in s: # convert IP to CIDR
                if s["ip"].find("/")<0:
                    s["ip"]=s["ip"]+"/32"
        dbp.ingest_bulk(sensors)

print("DB Initialized", flush=True)

