#!/usr/bin/python3

from subprocess import Popen,PIPE,STDOUT
from tornado import web,gen
from tornado.concurrent import run_on_executor
from concurrent.futures import ThreadPoolExecutor
import os

thumbnail_root="/var/www/thumbnail"
recording_root="/mnt/storage"

class ThumbnailHandler(web.RequestHandler):
    def __init__(self, app, request, **kwargs):
        super(ThumbnailHandler, self).__init__(app, request, **kwargs)
        self.executor= ThreadPoolExecutor(8)

    def check_origin(self, origin):
        return True

    def _run(self, cmd):
        with Popen(cmd,stdout=PIPE,stderr=STDOUT,bufsize=1,universal_newlines=True) as p:
            for line in p.stdout:
                yield line.strip()
            p.stdout.close()
            p.wait()

    @run_on_executor
    def _thumbnail(self, uri):
        thumbnail=uri.replace('/thumbnail/','')
        filename=thumbnail.replace('.png','')
        try:
            os.makedirs(thumbnail_root+'/'+('/'.join(thumbnail.split('/')[:-1])))
        except:
            pass

        for line in self._run(["/usr/bin/ffmpeg","-i",recording_root+"/"+filename,"-vf","thumbnail,scale=640:360","-frames:v","1",thumbnail_root+"/"+thumbnail]):
            pass
    
    @gen.coroutine
    def get(self):
        yield self._thumbnail(self.request.uri)
        self.add_header('X-Accel-Redirect',self.request.uri)
        self.set_status(200,'OK')
