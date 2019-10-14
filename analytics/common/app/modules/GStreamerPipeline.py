import string
import json
import time
import os
import copy
import modules.Destination as Destination  # pylint: disable=import-error
import modules.GstGVAJSONMeta as GstGVAJSONMeta  # pylint: disable=import-error
from modules.Pipeline import Pipeline  # pylint: disable=import-error
from modules.PipelineManager import PipelineManager  # pylint: disable=import-error
from modules.ModelManager import ModelManager  # pylint: disable=import-error
from common.utils import logging  # pylint: disable=import-error

import gi  # pylint: disable=import-error
gi.require_version('Gst', '1.0')
from gi.repository import Gst, GObject  # pylint: disable=import-error

logger = logging.get_logger('GSTPipeline', is_static=True)


class GStreamerPipeline(Pipeline):

    Gst.init(None)
    GObject.threads_init()
    GVA_INFERENCE_ELEMENT_TYPES = ["GstGvaDetect",
                                   "GstGvaClassify",
                                   "GstGvaInference"]


    def __init__(self, id, config, models, request):
        self.config = config
        self.id = id
        self.pipeline = None
        self.template = config['template']
        self.models = models
        self.request = request
        self.state = "QUEUED"
        self.frame_count = 0
        self.start_time = None
        self.stop_time = None
        self.avg_fps = 0
        self.destination = None
        self._gst_launch_string = None
        self.latency_times = dict()
        self.sum_pipeline_latency = 0
        self.count_pipeline_latency = 0

    def stop(self):
        if self.pipeline is not None:
            self.pipeline.set_state(Gst.State.NULL)
            if self.state is "RUNNING":
                self.state = "ABORTED"
                logger.debug("Setting Pipeline {id} State to ABORTED".format(id=self.id))
            self.stop_time = time.time()
            PipelineManager.pipeline_finished()
        if self.state is "QUEUED":
            self.state = "ABORTED"
            PipelineManager.remove_from_queue(self.id)
            logger.debug("Setting Pipeline {id} State to ABORTED and removing from the queue".format(id=self.id))


        del self.pipeline
        self.pipeline = None

        return self.status()

    def params(self):

        request = copy.deepcopy(self.request)
        del request["models"]

        params_obj = {
            "id": self.id,
            "request": request,
            "type": self.config["type"],
            "launch_command": self._gst_launch_string
        }

        return params_obj

    def status(self):
        logger.debug("Called Status")
        if self.stop_time is not None:
            elapsed_time = max(0, self.stop_time - self.start_time)
        elif self.start_time is not None:
            elapsed_time = max(0, time.time() - self.start_time)
        else:
            elapsed_time = None

        status_obj = {
            "id": self.id,
            "state": self.state,
            "avg_fps": self.avg_fps,
            "start_time": self.start_time,
            "elapsed_time": elapsed_time
        }
        if not self.count_pipeline_latency == 0:
            status_obj["avg_pipeline_latency"] = self.sum_pipeline_latency / self.count_pipeline_latency
        
        return status_obj

    def get_avg_fps(self):
        return self.avg_fps

    def _add_tags(self):
        if "tags" in self.request:
            metaconvert = self.pipeline.get_by_name("jsonmetaconvert")
            if metaconvert:
                metaconvert.set_property("tags", json.dumps(self.request["tags"]))
            else:
                logger.debug("tags given but no metaconvert element found")

    def _add_default_parameters(self):
        request_parameters = self.request.get("parameters", {})
        pipeline_parameters = self.config.get("parameters", {}).get("properties", {})

        for key in pipeline_parameters:
            if (not key in request_parameters) and ("default" in pipeline_parameters[key]):
                request_parameters[key] = pipeline_parameters[key]["default"]

        self.request["parameters"] = request_parameters

    def _add_element_parameters(self):
        request_parameters = self.request.get("parameters", {})
        pipeline_parameters = self.config.get("parameters", {}).get("properties", {})

        for key in pipeline_parameters:                
            if "element" in pipeline_parameters[key]:
                if key in request_parameters:
                    element = self.pipeline.get_by_name(pipeline_parameters[key]["element"])
                    if element:
                        element.set_property(key, request_parameters[key])
                    else:
                        logger.debug("parameter given for element but no element found")

    def _add_default_models(self):
        gva_elements = [e for e in self.pipeline.iterate_elements() if (e.__gtype__.name in self.GVA_INFERENCE_ELEMENT_TYPES and "VA_DEVICE_DEFAULT" in e.get_property("model"))]
        for e in gva_elements:
            network = ModelManager.get_default_network_for_device(e.get_property("device"),e.get_property("model"))
            logger.debug("Setting model to {} for element {}".format(network,e.get_name()))
            e.set_property("model",network)
            
    @staticmethod
    def validate_config(config):
        template = config["template"]
        pipeline = Gst.parse_launch(template)
        appsink = pipeline.get_by_name("appsink")
        jsonmetaconvert = pipeline.get_by_name("jsonmetaconvert")
        metapublish = pipeline.get_by_name("metapublish")
        if appsink is None:
            logger.warning("Missing appsink element")
        if jsonmetaconvert is None:
            logger.warning("Missing metaconvert element")
        if metapublish is None:
            logger.warning("Missing metapublish element")

    def calculate_times(self,sample):
        buffer = sample.get_buffer()
        segment = sample.get_segment()
        times={}
        times['segment.time'] = segment.time
        times['stream_time'] = segment.to_stream_time(Gst.Format.TIME,buffer.pts)                
        return times
        

    def format_location_callback (self,splitmux, fragment_id,sample,data=None):
        times=self.calculate_times(sample)

        if (self._real_base == None):
            clock = Gst.SystemClock(clock_type=Gst.ClockType.REALTIME)
            self._real_base = clock.get_time()
            self._stream_base = times["segment.time"]
            metaconvert = self.pipeline.get_by_name("jsonmetaconvert")
            
            if metaconvert:
                if ("tags" not in self.request):
                    self.request["tags"]={}
                self.request["tags"]["real_base"] = self._real_base
                metaconvert.set_property("tags", json.dumps(self.request["tags"]))

        adjusted_time = self._real_base + (times["stream_time"] - self._stream_base)
        self._year_base = time.strftime("%Y", time.localtime(adjusted_time / 1000000000))
        self._month_base = time.strftime("%m", time.localtime(adjusted_time / 1000000000))
        self._day_base = time.strftime("%d", time.localtime(adjusted_time / 1000000000))
        self._dirName = "%s/%s/%s/%s" %(self.request["parameters"]["recording_prefix"],self._year_base,self._month_base,self._day_base)

        try:
            os.makedirs(self._dirName)
        except FileExistsError:
            logger.debug("Directory already exists")

        return "%s/%d_%d.mp4" %(self._dirName,
                                adjusted_time,
                                times["stream_time"]-self._stream_base)


    def start(self):
        logger.debug("Starting Pipeline {id}".format(id=self.id))

        try:
            self.destination = Destination.create_instance(self.request)
        except:
            self.destination = None

        self.request["models"] = self.models
        self._add_default_parameters()
        self._gst_launch_string = string.Formatter().vformat(self.template, [], self.request)
        logger.debug(self._gst_launch_string)
        self.pipeline = Gst.parse_launch(self._gst_launch_string)
        self._add_element_parameters()
        self._add_tags()
        self._add_default_models()
        sink = self.pipeline.get_by_name("appsink")

        if sink is not None:
            sink.set_property("emit-signals", True)
            sink.set_property('sync', False)
            sink.connect("new-sample", GStreamerPipeline.on_sample, self)
            self.avg_fps= 0

        src = self.pipeline.get_by_name("source")
        
        if src and sink:
            src_pad = src.get_static_pad("src")
            if (src_pad):
                src_pad.add_probe(Gst.PadProbeType.BUFFER, GStreamerPipeline.source_probe_callback, self)
            else:
                src.connect("pad-added", GStreamerPipeline.source_pad_added_callback, self)
            sink_pad = sink.get_static_pad("sink")
            sink_pad.add_probe(Gst.PadProbeType.BUFFER, GStreamerPipeline.appsink_probe_callback, self)
            
        bus = self.pipeline.get_bus()
        bus.add_signal_watch()
        bus.connect("message", GStreamerPipeline.bus_call, self)
        splitmuxsink = self.pipeline.get_by_name("splitmuxsink")
        self._real_base=None

        if (splitmuxsink != None):
            splitmuxsink.connect("format-location-full",
                           self.format_location_callback,
                           None)

        self.pipeline.set_state(Gst.State.PLAYING)
        self.start_time = time.time()

    @staticmethod
    def source_pad_added_callback(element, pad, self):
        pad.add_probe(Gst.PadProbeType.BUFFER, GStreamerPipeline.source_probe_callback, self)
        return Gst.FlowReturn.OK
        

    @staticmethod
    def source_probe_callback(pad, info, self):
        buffer = info.get_buffer()
        pts = buffer.pts
        self.latency_times[pts] = time.time()
        return Gst.PadProbeReturn.OK

    @staticmethod
    def appsink_probe_callback(pad, info, self):
        buffer = info.get_buffer()
        pts = buffer.pts
        source_time = self.latency_times.pop(pts, -1)
        if not source_time == -1:
            self.sum_pipeline_latency += time.time() - source_time
            self.count_pipeline_latency += 1
        return Gst.PadProbeReturn.OK


    @staticmethod
    def on_sample(sink, self):

        logger.debug("Received Sample from Pipeline {id}".format(id=self.id))
        sample = sink.emit("pull-sample")
        try:

            buf = sample.get_buffer()
            try:
                meta = buf.get_meta("GstGVAJSONMetaAPI")
            except:
                meta = None

            if meta is None:
                logger.debug("No GstGVAJSONMeta")
            else:
                json_string = GstGVAJSONMeta.get_json_message(meta).decode('utf-8')  # pylint: disable=undefined-variable
                json_object = json.loads(json_string)
                #json_object['tags']={'times':self.calculate_times(sample)}
                logger.debug(json.dumps(json_object))
                if self.destination and ("objects" in json_object) and (len(json_object["objects"]) > 0):
                    self.destination.send(json_object)
        except Exception as error:
            logger.error("Error on Pipeline {id}: {err}".format(id=self.id, err=error))

        self.frame_count += 1
        self.avg_fps = self.frame_count/(time.time()-self.start_time)
        return Gst.FlowReturn.OK

    @staticmethod
    def bus_call(bus, message, self):
        t = message.type
        if t == Gst.MessageType.EOS:
            logger.info("Pipeline {id} Ended".format(id=self.id))
            self.pipeline.set_state(Gst.State.NULL)
            if self.state is "RUNNING":
                logger.debug("Setting Pipeline {id} State to COMPLETED".format(id=self.id))
                self.state = "COMPLETED"
            self.stop_time = time.time()
            bus.remove_signal_watch()
            if (self.destination):
                del self.destination
                self.destination=None
            del self.pipeline
            self.pipeline = None
            PipelineManager.pipeline_finished()
        elif t == Gst.MessageType.ERROR:
            err, debug = message.parse_error()
            logger.error("Error on Pipeline {id}: {err}".format(id=id, err=err))
            
            if (self.state is None) or (self.state is "RUNNING") or (self.state is "QUEUED"):
                logger.debug("Setting Pipeline {id} State to ERROR".format(id=self.id))
                self.stop_time = time.time()
                self.state = "ERROR"
            self.pipeline.set_state(Gst.State.NULL)
            self.stop_time = time.time()
            bus.remove_signal_watch()
            del self.pipeline
            self.pipeline = None
            PipelineManager.pipeline_finished()
        elif t == Gst.MessageType.STATE_CHANGED:
            old_state, new_state, pending_state = message.parse_state_changed()
            if message.src == self.pipeline:
                if old_state == Gst.State.PAUSED and new_state == Gst.State.PLAYING:
                    if self.state is "QUEUED":
                        logger.debug("Setting Pipeline {id} State to RUNNING".format(id=self.id))
                        self.state = "RUNNING"
        else:
            pass
        return True
