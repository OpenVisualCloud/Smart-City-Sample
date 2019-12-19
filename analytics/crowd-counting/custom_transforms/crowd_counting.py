import gstgva
import numpy
import time
import json
from PIL import Image, ImageDraw

class CrowdCounting:
    def __init__(self,zone=0,width=1280,height=720, polygon=[1080,200,1166,200,1166,216,1211,216,1211,523,1167,523,1167,530,1080,530,1080,200]):
        print("===========CrowdCounting:__init__:zone,width,height,polygon=", zone, width, height, polygon, "================")

        # # #this is for 1280x720 sensor input
        # self.polygons=[0]*8
        # self.polygons[0] = [[1080,200],[1166,200],[1166,216],[1211,216],[1211,523],[1167,523],[1167,530],[1080,530],[1080,200]]
        # self.polygons[1] = [[1036,51],[1075,51],[1115,58],[1153,72],[1182,92],[1200,119],[1209,146],[1209,216],[1167,216],[1167,201],[1123,201],[1083,199],[1079,175],[1066,159],[1044,144],[1016,139],[946,139],[946,111],[991,111],[991,84],[1036,83],[1036,51]]
        # self.polygons[2] = [[314,52],[314,82],[336,82],[336,111],[395,111],[395,141],[947,141],[947,112],[993,112],[993,82],[1038,82],[1037,52],[314,52]]
        # self.polygons[3] = [[314,52],[314,82],[336,82],[336,111],[394,111],[394,139],[326,139],[298,141],[272,150],[254,165],[244,181],[244,202],[206,202],[204,204],[167,204],[167,155],[184,123],[216,101],[257,87],[278,83],[277,52],[314,52]]
        # self.polygons[4] = [[163,533],[207,533],[247,525],[247,201],[163,201],[163,533]]
        # self.polygons[5] = [[247,525],[206,531],[166,531],[166,559],[186,587],[216,609],[254,623],[293,627],[363,626],[363,600],[398,600],[398,570],[329,570],[299,568],[274,560],[258,544],[247,525]]
        # self.polygons[6] = [[950,569],[950,598],[983,598],[983,626],[1012,626],[1012,655],[317,655],[317,626],[363,626],[363,598],[398,598],[398,569],[950,569]]
        # self.polygons[7] = [[1208,523],[1208,546],[1205,574],[1193,602],[1166,629],[1125,647],[1082,654],[1011,654],[1011,628],[983,628],[983,600],[950,600],[950,570],[1019,570],[1048,563],[1070,548],[1084,528],[1120,536],[1125,529],[1166,529],[1166,523],[1208,523]]

        self.zone = zone
        self.mask=[0]
        self.crowd_count=0
        self.polygon=polygon
        
        # model resolution 128x96
        # adjust polygon size to model resolution
        self.width = 128
        self.height = 96
        self.ratioX = self.width * 1.0 / width
        self.ratioY = self.height * 1.0 / height
        for t in range(len(self.polygon)>>1):
            self.polygon[t<<1] = int(self.polygon[t<<1] * self.ratioX)
            self.polygon[(t<<1)+1] = int(self.polygon[(t<<1)+1] * self.ratioY)
        
        #convert polygon to mask algorithm
        #https://stackoverflow.com/questions/3654289/scipy-create-2d-polygon-mask
        self.img = Image.new('L', (self.width, self.height), 0)
        ImageDraw.Draw(self.img).polygon(self.polygon, outline=1, fill=1)
        self.mask = numpy.array(self.img).flatten()

    def process_frame(self, frame):
        for tensor in frame.tensors():
            data = tensor.data()
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
