#!/usr/bin/python3

from tornado import web, gen
from tornado.concurrent import run_on_executor
from concurrent.futures import ThreadPoolExecutor
from probe import run
from configuration import env
import uuid
import os

THUMBNAIL_CACHE=int(env["THUMBNAIL_CACHE"])

class Thumbnail(object):
    def __init__(self):
        self._cache=[]

    def get_thumbnail(self, mp4, size, start_time):
        for c in self._cache:
            if c[0]==mp4 and c[1]==size and c[2]==start_time: 
                return c[3]

        png="/tmp/"+str(uuid.uuid4())+".png"
        cmds=["/usr/local/bin/ffmpeg"]
        if start_time: cmds.extend(["-ss","{:02d}:{:02d}:{:02d}.{:03d}".format(int(start_time/3600000),int(start_time/60000),int(start_time/1000),int(start_time%1000))])
        cmds.extend(["-i",mp4])
        if size: cmds.extend(["-vf","scale="+size])
        cmds.extend(["-frames:v","1",png])

        try:
            list(run(cmds))
            with open(png,"rb") as fd:
                image=fd.read()
        except Exception as e:
            print(str(e), flush=True)
            if not start_time: return None
            cmds[1:3]=["-sseof","-1"]
            cmds[-3:-1]=["-update","1","-vsync","0"]
            try:
                list(run(cmds))
                with open(png,"rb") as fd:
                    image=fd.read()
            except Exception as e:
                print(str(e), flush=True)
                return None

        try:
            os.remove(png)
        except:
            pass 

        if len(self._cache)>THUMBNAIL_CACHE: self._cache.pop(0)
        self._cache.append((mp4,size,start_time,image))
        return image
    
thumbnail=Thumbnail()

class ThumbnailHandler(web.RequestHandler):
    def __init__(self, app, request, **kwargs):
        super(ThumbnailHandler, self).__init__(app, request, **kwargs)
        self.executor= ThreadPoolExecutor(4)
        self._storage = "/var/www/mp4"

    def check_origin(self, origin):
        return True

    @run_on_executor
    def _mp4ToPNG(self, mp4, size, start_time):
        return thumbnail.get_thumbnail(mp4, size, start_time)
                        
    @gen.coroutine
    def get(self):
        mp4=self.request.uri.replace("/api/thumbnail",self._storage).split("?")[0]
        size=self.get_argument("size","")
        start_time=float(self.get_argument("start_time","0"))
        png=yield self._mp4ToPNG(mp4,size,start_time)
        if png:
            self.write(png)
            self.set_header("Content-Type","image/png")
        else:
            self.set_status(400, "Not Found")
