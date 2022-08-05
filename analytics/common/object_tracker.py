#!/usr/bin/python3
import traceback
from threading import Thread, Condition, Timer
from signal import signal, SIGTERM
from configuration import env
import json
import time
import datetime
import sys
import struct
from iou_tracker import IOUTracker
from bb_utils import BBUtil

class OT(object):
    def __init__(self):
        super(OT, self).__init__()

        self._tracker={}

    def tracking(self,metadata):

        sensor=metadata["tags"]["sensor"]
        if sensor not in self._tracker:
            self._tracker[sensor]=IOUTracker(sigma_l=0,sigma_h=0.5,sigma_iou=0.5,t_min=2)

        tracker=self._tracker[sensor]

        width = metadata["resolution"]["width"]
        height = metadata["resolution"]["height"]
        bbutil=BBUtil(width, height)

        objects=metadata["objects"]
        bboxs=[]
        confidence=[]
        object_type=[]
        detections=[]
        for _idx in range(len(objects)):
            bbox=objects[_idx]["detection"]["bounding_box"]
            bbox=[bbox["x_min"],bbox["y_min"],bbox["x_max"],bbox["y_max"]]
            bboxs=bbutil.float_to_int(bbox)
            detections += [{
                "bbox":bbox,
                "confidence": objects[_idx]["detection"]["confidence"],
                "object_type": objects[_idx]["detection"]["label_id"],
                "idx": _idx,
                }]

        results=[]
        t=time.time()
        results=tracker.track(detections)
        #print("mot: ",int((time.time()-t)*1000),sensor,flush=True)

        if len(results) == 0: return
        for item in results:
           objects[item["idx"]]["track_id"]=item["track_id"]
        metadata["objects"]=[objects[item["idx"]] for item in results]
        metadata["nobjects"]=len(results)
        
        return metadata



