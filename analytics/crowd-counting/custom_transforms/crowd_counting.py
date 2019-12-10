import gstgva
import numpy
import time
import logging
import json

class CrowdCounting:

    def __init__(self):
        self.init_logging()
        self.log.debug("============custom transform: __init__============")
        
    def init_logging(self):
        self.log = logging.getLogger("crowd_counting")
        self.log.setLevel(logging.DEBUG) #NOTEST, DEBUG, INFO, WARNING, ERROR, CRITICAL
        self.log.addHandler(logging.StreamHandler())

    def process_frame(self, frame):
        crowd_count = 0
        for tensor in frame.tensors():
            data = tensor.data()
            self.log.debug("============custom transform: data============")
            #1/8 of image resolution, 768x1024 image, data is 1x96x128x1
            print(data)
            crowd_count = numpy.sum(data)

        if (crowd_count):
            region = frame.add_region("zone0",0,0,100,100)
            count_tensor = region.add_tensor("crowd_count")
            count_tensor.set_label(str(crowd_count))
            count_tensor["model_name"] = "model_A_weights"

        # if (crowd_count):
            # messages = list(frame.messages())
            # self.log.info("============crowd_count={}============".format(crowd_count))
            # if len(messages) > 0:
                # self.log.info("============set_message============")
                # json_msg = json.loads(messages[0].get_message())
                # json_msg["time"] = float(time.time())
                # json_msg["count"] = {"zone0":crowd_count}
                # messages[0].set_message(json.dumps(json_msg))
            # else:
                # self.log.info("============add_message============")
                # crowd_msg = {'zone0':float(crowd_count)}
                # json_msg = {'time': int(time.time()), 'count':crowd_msg}
                # frame.add_message(json.dumps(json_msg))
                
        return True
