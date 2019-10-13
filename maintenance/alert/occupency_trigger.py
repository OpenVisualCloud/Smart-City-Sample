#!/usr/bin/python3

from db_query import DBQuery
from trigger import Trigger
import time
import os

office=list(map(float,os.environ["OFFICE"].split(",")))
service_interval=list(map(float,os.environ["SERVICE_INTERVAL"].split(",")))
args=list(map(float,os.environ["OCCUPENCY_ARGS"].split(",")))
dbhost=os.environ["DBHOST"]

class OccupencyTrigger(Trigger):
   def __init__(self):
       super(OccupencyTrigger,self).__init__()
       self._db=DBQuery(index="analytics",office=office,host=dbhost)

   def trigger(self):
       time.sleep(service_interval[0])
       objects=("",0)
       seats=("",0)
       people=("",0)
       try:
           for q in self._db.search("time>=now-"+str(args[0])+" and (nobjects>"+str(args[1])+" or count.people>"+str(args[2])+" or nseats>"+str(args[3])+")",size=25):

               if "nobjects" in q["_source"]:
                   if q["_source"]["nobjects"]>objects[1]:
                       objects=(q["_source"]["location"],q["_source"]["nobjects"])

               if "nseats" in q["_source"]:
                   if q["_source"]["nseats"]>seats[1]:
                       seats=(q["_source"]["location"],q["_source"]["nseats"])

               if "count" in q["_source"]:
                   if "people" in q["_source"]["count"]:
                       if q["_source"]["count"]["people"]>people[1]:
                           people=(q["_source"]["location"],q["_source"]["count"]["people"])

       except Exception as e:
           print("Exception: "+str(e), flush=True)

       info=[]
       if objects[1]>0: 
           info.append({
               "location": objects[0],
               "warning": [{
                   "message": "Traffic busy: #objects="+str(objects[1]),
                   "args": {
                       "nobjects": objects[1],
                   },
               }],
           })
       if people[1]>0:
           info.append({
               "location": people[0],
               "warning": [{
                   "message": "Entrence crowded: #people="+str(people[1]),
                   "args": {
                       "occupency": people[1],
                   }
               }],
           })
       if seats[1]>0: 
           info.append({
               "location": seats[0],
               "warning": [{
                   "message": "Zone crowded: #seats="+str(seats[1]),
                   "args": {
                       "nseats": seats[1],
                   }
               }],
           })
       return info
