'''
* Copyright (C) 2019 Intel Corporation.
* 
* SPDX-License-Identifier: BSD-3-Clause
'''

import os
import json
import common.settings  # pylint: disable=import-error
from common.utils import logging  # pylint: disable=import-error
import time
from modules.ModelManager import ModelManager  # pylint: disable=import-error
from collections import deque
import jsonschema as jsonschema
import modules.schema as schema
import tornado

logger = logging.get_logger('PipelineManager', is_static=True)

def import_pipeline_types():
    pipeline_types = {}
    try:
        from modules.GStreamerPipeline import GStreamerPipeline  # pylint: disable=import-error
        pipeline_types['GStreamer'] = GStreamerPipeline
    except Exception as error:
        logger.error("Error loading GStreamer: %s\n" % (error,))
    try:
        from modules.FFmpegPipeline import FFmpegPipeline  # pylint: disable=import-error
        pipeline_types['FFmpeg'] = FFmpegPipeline
    except Exception as error:
        logger.error("Error loading FFmpeg: %s\n" % (error,))

    return pipeline_types


class PipelineManager:
    MAX_RUNNING_PIPELINES = -1
    running_pipelines = 0
    pipeline_types = {}
    pipeline_instances = {}
    pipeline_state = {}
    pipeline_id = 0
    pipelines = None
    pipeline_queue = deque()

    @staticmethod
    def load_config(pipeline_dir, max_running_pipelines):
        PipelineManager.pipeline_types = import_pipeline_types()
        logger.info("Loading Pipelines from Config Path {path}".format(path=pipeline_dir))
        if os.path.islink(pipeline_dir):
            logger.warning("Pipelines directory is symbolic link")
        if os.path.ismount(pipeline_dir):
            logger.warning("Pipelines directory is mount point")
        PipelineManager.MAX_RUNNING_PIPELINES = max_running_pipelines
        pipelines = {}
        for root, subdirs, files in os.walk(pipeline_dir):
            if os.path.abspath(root) == os.path.abspath(pipeline_dir):
                for subdir in subdirs:
                    pipelines[subdir] = {}
            else:
                if len(files) == 0:
                    pipeline = os.path.basename(root)
                    pipelines[pipeline] = {}
                    for subdir in subdirs:
                        pipelines[pipeline][subdir] = {}
                else:
                    pipeline = os.path.basename(os.path.dirname(root))
                    version = os.path.basename(root)
                    for file in files:
                        path = os.path.join(root, file)
                        if path.endswith(".json"):
                            with open(path, 'r') as jsonfile:
                                config = json.load(jsonfile)
                                if ('type' not in config) or ('description' not in config) :
                                    logger.warning("Skipping loading of pipeline %s because of missing type or description" % (pipeline))
                                    continue
                                if config['type'] in PipelineManager.pipeline_types:
                                    pipelines[pipeline][version] = config
                                    # validate_config will throw warning of missing elements but continue execution
                                    PipelineManager.pipeline_types[config['type']].validate_config(config)
                                else:
                                    del pipelines[pipeline][version]
                                    logger.error("Pipeline %s with type %s not supported" % (pipeline, config['type']))
        # Remove pipelines with no valid versions
        pipelines = dict([(model, versions) for model, versions in pipelines.items() if len(versions) > 0])
        PipelineManager.pipelines = pipelines
        logger.info("Completed Loading Pipelines")

    @staticmethod
    def get_loaded_pipelines():
        results = []
        if PipelineManager.pipelines is not None:
            for pipeline in PipelineManager.pipelines:
                for version in PipelineManager.pipelines[pipeline]:
                    result = PipelineManager.get_pipeline_parameters(pipeline, version)
                    if result:
                        results.append(result)
        return results

    @staticmethod
    def get_pipeline_parameters(name, version):
        if not PipelineManager.pipeline_exists(name, version):
            return None
        params_obj = {
            "name": name,
            "version": version
        }
        if "type" in PipelineManager.pipelines[name][version]:
            params_obj["type"] = PipelineManager.pipelines[name][version]["type"]
        if "description" in PipelineManager.pipelines[name][version]:
            params_obj["description"] = PipelineManager.pipelines[name][version]["description"]
        if "parameters" in PipelineManager.pipelines[name][version]:
            params_obj["parameters"] = PipelineManager.pipelines[name][version]["parameters"]
        return params_obj

    @staticmethod
    def is_input_valid(request,pipeline_config,section):
        config = pipeline_config.get(section,{})
        try:
            if (section in request):
                input_validator = jsonschema.Draft4Validator(schema=config, format_checker=jsonschema.draft4_format_checker)
                input_validator.validate(request.get(section, {}))    
                logger.debug("{} Validation successful".format(section))
            return True
        except Exception as error:
            logger.debug("Validation error in request section {} payload".format(section))
            return False

    @staticmethod
    def get_section_and_config(request,config,request_section=[],config_section=[]):
        for key in request_section:
            request = request.get(key,{})

        for key in config_section:
            config = config.get(key,{})
       
        return request,config

    @staticmethod
    def set_section_defaults(request,config,request_section=[],config_section=[]):        
        section,config = PipelineManager.get_section_and_config(request,config,request_section,config_section)
        for key in config:
            if (key not in section) and ("default" in config[key]):
                section[key] = config[key]["default"]

        if (len(section)):
            result = request
            for key in request_section[0:-1]:
                result=result.setdefault(key,{})
            result[request_section[-1]]=section

    @staticmethod
    def set_defaults(request,config):

        if ("destination" not in config):
            config["destination"]=schema.destination
        if ("source" not in config):
            config["source"] = schema.source
        if ("tags" not in config):
            config["tags"]=schema.tags

        PipelineManager.set_section_defaults(request,config,["parameters"],
                                             ["parameters","properties"])
        if ("destination" in request) and ("type" in request["destination"]):
            PipelineManager.set_section_defaults(request,config,["destination"],
                                                 ["destination",request["destination"]["type"],"properties"])
        if ("source" in request) and ("type" in request["source"]):
            PipelineManager.set_section_defaults(request,config,["source"],
                                                 ["source",request["source"]["type"],"properties"])

        PipelineManager.set_section_defaults(request,config,["tags"],
                                              ["tags","properties"])


    @staticmethod
    def create_instance(name, version, request):
        logger.info("Creating Instance of Pipeline {name}/{v}".format(name=name, v=version))
        if not PipelineManager.pipeline_exists(name, version):
            return None, "Invalid Pipeline or Version"

        pipeline_type = PipelineManager.pipelines[name][str(version)]['type']
        pipeline_config = PipelineManager.pipelines[name][str(version)]

        PipelineManager.set_defaults(request,pipeline_config)

        if not PipelineManager.is_input_valid(request,pipeline_config,"parameters"):
            return None, "Invalid Parameters"
        if not PipelineManager.is_input_valid(request,pipeline_config,"destination"):
            return None, "Invalid Destination"
        if not PipelineManager.is_input_valid(request,pipeline_config,"source"):
            return None, "Invalid Source"
        if not PipelineManager.is_input_valid(request,pipeline_config,"tags"):
            return None, "Invalid Tags"
        
        PipelineManager.pipeline_id += 1
        
        PipelineManager.pipeline_instances[PipelineManager.pipeline_id] = \
            PipelineManager.pipeline_types[pipeline_type](PipelineManager.pipeline_id,
                                                          pipeline_config,
                                                          ModelManager.models,
                                                          request)
        PipelineManager.pipeline_queue.append(PipelineManager.pipeline_id)
        PipelineManager.start()
        return PipelineManager.pipeline_id, None

    @staticmethod
    def start():
        if (PipelineManager.MAX_RUNNING_PIPELINES <= 0 or PipelineManager.running_pipelines < PipelineManager.MAX_RUNNING_PIPELINES) and len(PipelineManager.pipeline_queue) != 0:
            pipeline_to_start = PipelineManager.pipeline_instances[PipelineManager.pipeline_queue.popleft()]
            if(pipeline_to_start is not None):
                PipelineManager.running_pipelines += 1
                pipeline_to_start.start()

    @staticmethod
    def start_next_pipeline():
        PipelineManager.running_pipelines -= 1
        PipelineManager.start()

    @staticmethod
    def pipeline_finished():
        ioloop = tornado.ioloop.IOLoop.instance()
        ioloop.add_callback(PipelineManager.start_next_pipeline)

    @staticmethod
    def get_instance_parameters(name, version, instance_id):
        if PipelineManager.instance_exists(name, version, instance_id):
            return PipelineManager.pipeline_instances[instance_id].params()
        return None
        
    @staticmethod
    def get_instance_status(name, version, instance_id):
        if PipelineManager.instance_exists(name, version, instance_id):
            return PipelineManager.pipeline_instances[instance_id].status()
        return None

    @staticmethod
    def stop_instance(name, version, instance_id):
        if PipelineManager.instance_exists(name, version, instance_id):
            try:
                PipelineManager.pipeline_queue.remove(instance_id)
            except ValueError:
                pass
            finally:
                return PipelineManager.pipeline_instances[instance_id].stop()
        return None

    @staticmethod
    def instance_exists(name, version, instance_id):
        if PipelineManager.pipeline_exists(name, version) and instance_id in PipelineManager.pipeline_instances:
            return True
        logger.warning("Invalid Instance ID")
        return False
    @staticmethod
    def pipeline_exists(name, version):
        if name in PipelineManager.pipelines and str(version) in PipelineManager.pipelines[name]:
            return True
        logger.warning("Invalid pipeline or version")
        return False
