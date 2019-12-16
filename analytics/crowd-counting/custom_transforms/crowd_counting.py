import gstgva
import numpy
import time
import json
from PIL import Image, ImageDraw

class CrowdCounting:
    def __init__(self):
        self.numZone = 8
        self.mask=[0]*self.numZone
        self.crowd_count=[0]*self.numZone
        self.polygon=[0]*self.numZone
        
        #self._sensor = sensor
        self.polygon[0] = [865,210,933,210,933,227,968,227,968,560,934,560,934,568,865,568,865,210]
        self.polygon[1] = [830,49,861,49,893,56,922,71,946,93,960,122,967,151,967,228,934,228,934,211,899,211,867,209,864,183,854,165,836,149,814,144,759,144,759,114,795,114,795,84,830,83,830,49]
        self.polygon[2] = [259,49,259,82,277,82,277,114,323,114,323,146,760,146,760,114,796,114,796,82,832,82,831,49,259,49]
        self.polygon[3] = [259,49,259,82,277,82,277,114,322,114,322,144,269,144,246,146,226,156,212,173,204,190,204,212,174,212,172,214,143,214,143,161,157,127,182,103,214,87,231,83,230,49,259,49]
        self.polygon[4] = [140,571,174,571,206,563,206,211,140,211,140,571]
        self.polygon[5] = [206,563,174,569,142,569,142,599,158,630,182,654,212,668,242,673,298,672,298,644,326,644,326,612,271,612,248,609,227,600,215,583,206,563]
        self.polygon[6] = [762,611,762,642,788,642,788,672,811,672,811,704,261,704,261,672,298,672,298,642,325,642,325,611,762,611]
        self.polygon[7] = [966,561,966,586,964,615,954,646,933,676,900,695,866,702,810,702,788,674,788,644,762,644,762,611,817,611,840,604,857,587,868,566,896,574,901,567,933,567,933,561,966,561]

        #no matter what resolution the input video is (currently 720x1280),
        #it will resize to 1024x768 before sending to model
        #AI data input is 1/8 of image resolution, 768x1024 image, data is 1x96x128x1
        self.width = 1024>>3
        self.height = 768>>3
        for zone in range(self.numZone):
            for t in range(len(self.polygon[zone])):
                self.polygon[zone][t] = self.polygon[zone][t]>>3

        #convert polygon to mask algorithm
        #https://stackoverflow.com/questions/3654289/scipy-create-2d-polygon-mask
        self.img = Image.new('L', (self.width, self.height), 0)
        for zone in range(self.numZone):
            self.img = Image.new('L', (self.width, self.height), 0)
            ImageDraw.Draw(self.img).polygon(self.polygon[zone], outline=1, fill=1)
            self.mask[zone] = numpy.array(self.img).flatten()

    def process_frame(self, frame):
        for tensor in frame.tensors():
            data = tensor.data()
            imgData = []
            imgData.append(tensor.data())
            for zone in range(self.numZone):
                self.crowd_count[zone] = numpy.sum(self.mask[zone] * imgData)

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
