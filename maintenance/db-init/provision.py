#!/usr/bin/python3

from db_ingest import DBIngest
from configuration import env
import json

dbhost=env["DBHOST"]
office=list(map(float,env["OFFICE"].split(",")))
gwhost=env.get("GWHOST",None)
scenario=env["SCENARIO"]

def Provision(officestr):
    print("Provisioning...", flush=True)

    # populate db with simulated offices and provisionings
    with open("/run/secrets/sensor-info.json",encoding='utf-8') as fd:
        data=json.load(fd)
        dbp=DBIngest(index="provisions", office=office, host=dbhost)
        for office1 in data:
            if scenario != office1["scenario"]: continue
            location1=office1["location"]
            if location1["lat"]!=office[0] or location1["lon"]!=office[1]: continue

            sensors=office1.pop("sensors")
            for s in sensors: 
                s["office"]=location1
                if "ip" in s: # convert IP to CIDR
                    if s["ip"].find("/")<0:
                        s["ip"]=s["ip"]+"/32"
                    s["ip_text"]=s["ip"]  # dup for terms aggs
            dbp.ingest_bulk(sensors, refresh="wait_for")

            office1.pop("scenario")
            office1["uri"]=gwhost
            return office1

    raise Exception("Should not be here.")

