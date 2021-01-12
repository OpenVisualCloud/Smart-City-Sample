
class BBUtil(object):
    def __init__(self,width,height):
        super(BBUtil, self).__init__()
        self.width=width
        self.height=height

    def xywh_to_tlwh(self, bbox_xywh):
        x,y,w,h = bbox_xywh
        xmin = max(int(round(x - (w / 2))),0)
        ymin = max(int(round(y - (h / 2))),0)
        return [xmin,ymin,int(w),int(h)]

    def tlwh_to_xyxy(self, bbox_tlwh):
        x,y,w,h = bbox_tlwh
        x1 = max(int(x),0)
        x2 = min(int(x+w),self.width-1)
        y1 = max(int(y),0)
        y2 = min(int(y+h),self.height-1)
        return [x1,y1,x2,y2]

    def xywh_to_xyxy(self, bbox_xywh):
        x,y,w,h = bbox_xywh
        x1 = max(int(x-w/2),0)
        x2 = min(int(x+w/2),self.width-1)
        y1 = max(int(y-h/2),0)
        y2 = min(int(y+h/2),self.height-1)
        return [x1,y1,x2,y2]

    def xyxy_to_tlwh(self, bbox_xyxy):
        x1,y1,x2,y2 = bbox_xyxy
        t = x1
        l = y1
        w = int(x2-x1)
        h = int(y2-y1)
        return [t,l,w,h]

    def float_to_int(self,bbox_xyxy):
        x1,y1,x2,y2 = bbox_xyxy
        return [int(x1*self.width), int(y1*self.height), int(x2*self.width), int(y2*self.height)]

    def int_to_float(self,bbox_xyxy):
        x1,y1,x2,y2 = [float(item) for item in bbox_xyxy]
        return [x1/self.width, y1/self.height, x2/self.width, y2/self.height]
