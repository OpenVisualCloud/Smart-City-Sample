import gstgva
import numpy
import time
import json
from PIL import Image, ImageDraw

class CrowdCounting:
    def __init__(self,zone=0,width=0,height=0, polygon=[]):
        self.zone = zone
        self.mask=[0]
        self.crowd_count=0
        self.polygon=polygon

        self.sensor_width = width
        self.sensor_height = height
        self.model_width = 0
        self.model_height = 0

    def process_frame(self, frame):
        for tensor in frame.tensors():
            if (self.model_width == 0):
                #generate bitmask
                self.model_height = tensor.dims()[1]
                self.model_width = tensor.dims()[2]
                self.ratioX = self.model_width * 1.0 / self.sensor_width
                self.ratioY = self.model_height * 1.0 / self.sensor_height
                
                for t in range(len(self.polygon)>>1):
                    self.polygon[t<<1] = int(self.polygon[t<<1] * self.ratioX)
                    self.polygon[(t<<1)+1] = int(self.polygon[(t<<1)+1] * self.ratioY)

                #convert polygon to mask algorithm
                #https://stackoverflow.com/questions/3654289/scipy-create-2d-polygon-mask
                self.img = Image.new('L', (self.model_width, self.model_height), 0)
                ImageDraw.Draw(self.img).polygon(self.polygon, outline=1, fill=1)
                self.mask = numpy.array(self.img).flatten()

            else:
                #zone based crowd counting
                imgData = []
                imgData.append(tensor.data())
                self.crowd_count = numpy.sum(self.mask * imgData)

        if (self.crowd_count):
            messages = list(frame.messages())
            if len(messages) > 0:
                json_msg = json.loads(messages[0].get_message())
                json_msg["count"] = {"zone"+str(self.zone):int(self.crowd_count)}
                messages[0].set_message(json.dumps(json_msg))
                
        return True