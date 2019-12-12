import gstgva
import numpy
import time
import logging
import json

class CrowdCounting:

    def __init__(self):
        self.init_logging()
        self.log.debug("============custom transform: __init__============")
        #create bitmask here
        self.bitmask=[]
        self.crowd_count=[0]*8
        
    def init_logging(self):
        self.log = logging.getLogger("crowd_counting")
        self.log.setLevel(logging.DEBUG) #NOTEST, DEBUG, INFO, WARNING, ERROR, CRITICAL
        self.log.addHandler(logging.StreamHandler())

    def process_frame(self, frame):
        for tensor in frame.tensors():
            data = tensor.data()
            #1/8 of image resolution, 768x1024 image, data is 1x96x128x1
            for i in range(8):
                self.crowd_count[i] = numpy.sum(data)

        if (self.crowd_count):
            messages = list(frame.messages())
            #self.log.info("============len(crowd_count)={}============".format(len(self.crowd_count)))
            if len(messages) > 0:
                json_msg = json.loads(messages[0].get_message())
                json_msg["count"] = {
                    "zone0":int(self.crowd_count[0]),
                    "zone1":int(self.crowd_count[1]),
                    "zone2":int(self.crowd_count[2]),
                    "zone3":int(self.crowd_count[3]),
                    "zone4":int(self.crowd_count[4]),
                    "zone5":int(self.crowd_count[5]),
                    "zone6":int(self.crowd_count[6]),
                    "zone7":int(self.crowd_count[7])
                }
                messages[0].set_message(json.dumps(json_msg))
            else:
                self.log.debug("No JSON messages in frame")
                
        return True
