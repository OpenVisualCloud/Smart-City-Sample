import gstgva
import numpy
import time
import json
from PIL import Image, ImageDraw

class CrowdCounting:
    def __init__(self):
        self.mask=[]
        self.crowd_count=[0]*8
        self.polygon=[0]*8
        
        print("=================CrowdCounting:__init__================")
        #self._sensor = sensor
        self.width = 768
        self.height = 1024
        self.polygon[0] = [210,865,210,933,227,933,227,968,560,968,560,934,568,934,568,865,210,865]
        self.polygon[1] = [49,830,49,861,56,893,71,922,93,946,122,960,151,967,228,967,228,934,211,934,211,899,209,867,183,864,165,854,149,836,144,814,144,759,114,759,114,795,84,795,83,830,49,830]
        self.polygon[2] = [49,259,82,259,82,277,114,277,114,323,146,323,146,760,114,760,114,796,82,796,82,832,49,831,49,259]
        self.polygon[3] = [49,259,82,259,82,277,114,277,114,322,144,322,144,269,146,246,156,226,173,212,190,204,212,204,212,174,214,172,214,143,161,143,127,157,103,182,87,214,83,231,49,230,49,259]
        self.polygon[4] = [571,140,571,174,563,206,211,206,211,140,571,140]
        self.polygon[5] = [563,206,569,174,569,142,599,142,630,158,654,182,668,212,673,242,672,298,644,298,644,326,612,326,612,271,609,248,600,227,583,215,563,206]
        self.polygon[6] = [611,762,642,762,642,788,672,788,672,811,704,811,704,261,672,261,672,298,642,298,642,325,611,325,611,762]
        self.polygon[7] = [561,966,586,966,615,964,646,954,676,933,695,900,702,866,702,810,674,810,674,788,644,788,644,762,611,762,611,817,604,840,587,857,566,868,574,896,567,901,567,933,561,933,561,966]

        #no matter what resolution the input video is (currently 720x1280),
        #it will resize to 1024x768 before sending to model
        #1/8 of image resolution, 768x1024 image, data is 1x96x128x1
        #convert polygon to mask algorithm
        #https://stackoverflow.com/questions/3654289/scipy-create-2d-polygon-mask
        self.img = Image.new('L', (self.width, self.height), 0)
        for zone in range(8):
            ImageDraw.Draw(self.img).polygon(self.polygon[zone], outline=zone+1, fill=zone+1)
        self.mask = numpy.array(self.img)

    def process_frame(self, frame):
        for tensor in frame.tensors():
            data = tensor.data()
            #no matter what resolution the input video is (currently 720x1280),
            #it will resize to 1024x768 before sending to model
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
                print("=================zone0=", int(self.crowd_count[0]), "================")
            else:
                print("No JSON messages in frame")
                
        return True
