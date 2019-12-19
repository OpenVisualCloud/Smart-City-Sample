#!/usr/bin/python3

from trigger import Trigger
import psutil
import time
import os

service_interval=list(map(float,os.environ["SERVICE_INTERVAL"].split(",")))

class CPUTrigger(Trigger):
    def __init__(self):
        super(CPUTrigger,self).__init__()

    def trigger(self):
        time.sleep(service_interval[1])
        workload={
            "args": {
                "cpu": psutil.cpu_percent(),
            },
        }
        if workload["args"]["cpu"]>90:
            workload["message"]="Server overload: "+str(workload["args"]["cpu"])+"%"
            return [{ "fatal": [workload] }]
        elif workload["args"]["cpu"]>80:
            workload["message"]="Server busy: "+str(workload["args"]["cpu"])+"%"
            return [{ "warning": [workload] }]
        return []
