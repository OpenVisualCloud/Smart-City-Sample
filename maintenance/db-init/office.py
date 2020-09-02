#!/usr/bin/python3

from db_ingest import DBIngest
import os
import requests

dbhost=os.environ["DBHOST"]
dbseeds=os.environ["DBSEEDS"].split(",")
dbchost=os.environ["DBCHOST"]

def _set_remote(host, cluster_name, seeds, skip=True, ping="30s", compress=True):
    r=requests.put(host+"/_cluster/settings",json={
        "persistent": {
            "cluster": {
                "remote": {
                    cluster_name: {
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
        # register the local DB to the remote DB.
        _set_remote(dbchost,officestr[1:],dbseeds)
        
    # register office info
    dbo=DBIngest(index="offices",office="",host=dbchost)
    dbo.ingest(officeinfo, id1=officestr)

