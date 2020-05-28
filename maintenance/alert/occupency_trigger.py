#!/usr/bin/python3

from db_query import DBQuery
from trigger import Trigger
from language import text
import time
import os

office=list(map(float,os.environ["OFFICE"].split(",")))
service_interval=list(map(float,os.environ["SERVICE_INTERVAL"].split(",")))
args=os.environ["OCCUPENCY_ARGS"].split(",")
dbhost=os.environ["DBHOST"]

class OccupencyTrigger(Trigger):
   def __init__(self):
       super(OccupencyTrigger,self).__init__()
       self._db=DBQuery(index="analytics",office=office,host=dbhost)

   def trigger(self):
       time.sleep(service_interval[0])
       objects=("",0)
       crowd=("",0)
       entrance=("",0)
       svcq=("",0)
       try:
           for q in self._db.search("time>=now-"+args[0]+" and ((nobjects>"+args[1]+" and algorithm:'object') or (nobjects>"+args[2]+" and algorithm:'svcq') or (nobjects>"+args[3]+" and algorithm:'crowd') or (nobjects>"+args[4]+" and algorithm:'entrance'))",size=75):

               nobjects=q["_source"]["nobjects"]
               algorithm=q["_source"]["algorithm"]
               location=q["_source"]["location"]
               if algorithm.find("object")>=0:
                   if nobjects>objects[1]:
                       objects=(location,nobjects)
               elif algorithm.find("entrance")>=0:
                   if nobjects>entrance[1]:
                       entrance=(location,nobjects)
               elif algorithm.find("svcq")>=0:
                   if nobjects>svcq[1]:
                       svcq=(location,nobjects)
               elif algorithm.find("crowd")>=0:
                   if nobjects>crowd[1]:
                       crowd=(location,nobjects)

       except Exception as e:
           print("Exception: "+str(e), flush=True)

       info=[]
       if objects[1]>0: 
           info.append({
               "location": objects[0],
               "warning": [{
                   "message": text["traffic busy"].format(objects[1]),
                   "args": {
                       "nobjects": objects[1],
                   },
               }],
           })
       if entrance[1]>0:
           info.append({
               "location": entrance[0],
               "warning": [{
                   "message": text["entrance crowded"].format(entrance[1]),
                   "args": {
                       "occupency": entrance[1],
                   }
               }],
           })
       if svcq[1]>0:
           info.append({
               "location": svcq[0],
               "warning": [{
                   "message": text["service slow"].format(svcq[1]),
                   "args": {
                       "occupency": svcq[1],
                   }
               }],
           })
       if crowd[1]>0: 
           info.append({
               "location": crowd[0],
               "warning": [{
                   "message": text["seat crowded"].format(crowd[1]),
                   "args": {
                       "nseats": crowd[1],
                   }
               }],
           })

       return info
