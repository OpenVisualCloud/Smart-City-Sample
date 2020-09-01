#!/usr/bin/python3

from db_ingest import DBIngest
import os
import requests

dbhost=os.environ["DBHOST"]
dbseeds=os.environ["DBSEEDS"].split(",")
dbchost=os.environ["DBCHOST"]
dbcseeds=os.environ["DBCSEEDS"].split(",")

def _set_remote(host, cluster, seeds, skip=True, ping="30s", compress=True):
    r=requests.put(host+"/_cluster/settings",json={
        "persistent": {
            "cluster": {
                "remote": {
                    cluster[1:]: {
                        "seeds": seeds,
                        "skip_unavailable": skip,
                        "transport": {
                            "ping_schedule": ping,
                            "compress": compress,
                        },
                    },
                },
            },
        },
    })
    print(r.json(), flush=True)

def RegisterOffice(officestr, officeinfo):
    print("Register office...", flush=True)
    if dbhost!=dbchost:
        # register the cloud cluster to local DB.
        _set_remote(dbhost,"cloud",dbcseeds)

        # register the local cluster to remote DB.
        _set_remote(dbchost,officestr,dbseeds)
        
    # register office info
    dbo=DBIngest(index="offices",office="",host=dbchost)
    dbo.ingest(officeinfo, id1=officestr)

