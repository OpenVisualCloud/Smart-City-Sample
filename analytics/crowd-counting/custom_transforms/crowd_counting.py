import gstgva
import numpy
import time
import json

class CrowdCounting:

    def __init__(self):
        self.bitmask=[]
        self.crowd_count=[0]*8

    def process_frame(self, frame):
        for tensor in frame.tensors():
            data = tensor.data()
            #1/8 of image resolution, 768x1024 image, data is 1x96x128x1
            for i in range(8):
                self.crowd_count[i] = numpy.sum(data)

        if (self.crowd_count):
            messages = list(frame.messages())
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
                print("No JSON messages in frame")
                
        return True
