from modules.Pipeline import Pipeline  # pylint: disable=import-error
from modules.PipelineManager import PipelineManager  # pylint: disable=import-error
from modules.ModelManager import ModelManager  # pylint: disable=import-error
from common.utils import logging  # pylint: disable=import-error
import string
import shlex
import subprocess
import time
import copy
from threading import Thread
import shutil
import uuid
import re

logger = logging.get_logger('FFmpegPipeline', is_static=True)

if shutil.which('ffmpeg') is None:
    raise Exception("ffmpeg not installed")


class FFmpegPipeline(Pipeline):

    GVA_INFERENCE_FILTER_TYPES = ["detect",
                                  "classify"]

    DEVICEID_MAP = {2:'CPU',
                    3:'GPU',
                    5:'VPU',
                    6:'HDDL'}
    
    def __init__(self, id, config, models, request):
        self.config = config
        self.models = models
        self.template = config['template']
        self.id = id
        self._process = None
        self.start_time = None
        self.stop_time = None
        self._ffmpeg_launch_string = None
        self.request = request
        self.state = "QUEUED"
        self.fps = 0

    def stop(self):
        if self._process:
            self.state = "ABORTED"
            self._process.kill()
            logger.debug("Setting Pipeline {id} State to ABORTED".format(id=self.id))
            PipelineManager.pipeline_finished()
        if self.state is "QUEUED":
            PipelineManager.remove_from_queue(self.id)
            self.state = "ABORTED"
            logger.debug("Setting Pipeline {id} State to ABORTED and removing from the queue".format(id=self.id))


 
    def params(self):
        request = copy.deepcopy(self.request)
        del(request["models"])

        params_obj = {
            "id": self.id,
            "request": request,
            "type": self.config["type"],
            "launch_command": self._ffmpeg_launch_string
        }

        return params_obj

    def status(self):
        logger.debug("Called Status")
        if self.stop_time is not None:
            elapsed_time = self.stop_time - self.start_time
        elif self.start_time is not None:
            elapsed_time = time.time() - self.start_time
        else:
            elapsed_time = None
        status_obj = {
             "id": self.id,
             "state": self.state,
             "avg_fps": self.fps,
             "start_time": self.start_time,
             "elapsed_time": elapsed_time
         }

        return status_obj

    @staticmethod
    def validate_config(config):
        pass

    def _spawn(self,args):
        self.start_time = time.time()
        self._process=subprocess.Popen(args, stdout=subprocess.PIPE, stderr=subprocess.PIPE, bufsize=1, universal_newlines=True)
        self.state = "RUNNING"
        self._process.poll()
        while self._process.returncode == None:
            next_line = self._process.stderr.readline()
            fps_idx = next_line.rfind('fps=')
            q_idx = next_line.rfind('q=')
            if fps_idx != -1 and q_idx != -1:
                self.fps = int(float(next_line[fps_idx+4:q_idx].strip()))
            self._process.poll()
        self.stop_time = time.time()
        if self.state != "ABORTED":
            if self._process.returncode == 0:
                self.state = "COMPLETED"
            else:
                self.state = "ERROR"
            PipelineManager.pipeline_finished()
        self._process = None

    def _add_tags(self, iemetadata_args):
        if "tags" in self.request:
            try:
                for key in self.request["tags"]:
                    iemetadata_args.append("-custom_tag")
                    iemetadata_args.append("%s:%s," % (key, self.request["tags"][key]))
                if len(iemetadata_args):
                    # remove final comma
                    iemetadata_args[-1] = iemetadata_args[-1][:-1]
            except Exception:
                logger.error("Error adding tags")

    def _add_default_parameters(self):
        request_parameters = self.request.get("parameters", {})
        pipeline_parameters = self.config.get("parameters", {}).get("properties", {})

        for key in pipeline_parameters:
            if (not key in request_parameters) and ("default" in pipeline_parameters[key]):
                request_parameters[key] = pipeline_parameters[key]["default"]

        self.request["parameters"] = request_parameters

    def _get_filter_params(self,_filter):
        result = {}
        params = re.split("=|:",_filter)
        result['type'] = params[0]
        for x in range(1,len(params[0:]),2):
            result[params[x]] = params[x+1]
        return result

    def _join_filter_params(self,filter_params):
        filter_type = filter_params.pop('type')
        parameters = ["%s=%s" %(x,y) for (x,y) in filter_params.items()]
        return "%s=%s" %(filter_type,':'.join(parameters)) 
        
    def _add_default_models(self,args):
        vf_index = args.index('-vf') if ('-vf' in args) else None
        if (vf_index==None):
            return
        filters = args[vf_index+1].split(',')
        new_filters=[]
        for _filter in filters:
            filter_params = self._get_filter_params(_filter)
            if ( (filter_params['type'] in FFmpegPipeline.GVA_INFERENCE_FILTER_TYPES) and
                 ("VA_DEVICE_DEFAULT" in filter_params['model'])):
                device="CPU"
                if ("device" in filter_params):
                    device = FFmpegPipeline.DEVICEID_MAP[int(filter_params['device'])]
                filter_params["model"] = ModelManager.get_default_network_for_device(device,filter_params["model"])
                new_filters.append(self._join_filter_params(filter_params))
            else:
                new_filters.append(_filter)
        args[vf_index+1] =','.join(new_filters)
                
    def start(self):
        logger.debug("Starting Pipeline {id}".format(id=self.id))
        self.request["models"] = self.models

        self._add_default_parameters()
        self._ffmpeg_launch_string = string.Formatter().vformat(self.template, [], self.request)
        args = ['ffmpeg']
        args.extend(shlex.split(self._ffmpeg_launch_string))
        iemetadata_args = ["-f", "iemetadata", "-source_url", self.request["source"]["uri"]]

        self._add_tags(iemetadata_args)

        if 'destination' in self.request:
            if self.request['destination']['type'] == "kafka":
                for item in self.request['destination']['hosts']:
                    iemetadata_args.append("kafka://"+item+"/"+self.request["destination"]["topic"])
            elif self.request['destination']['type'] == "file":
                iemetadata_args.append(self.request['destination']['uri'])
        else:
            iemetadata_args.append("file:///tmp/tmp"+str(uuid.uuid4().hex)+".json")
                                    
        args.extend(iemetadata_args)
        self._add_default_models(args)
        logger.debug(args)
        thread = Thread(target=self._spawn, args=[args])
        thread.start()    
