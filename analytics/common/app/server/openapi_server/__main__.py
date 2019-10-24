#!/usr/bin/env python3
'''
* Copyright (C) 2019 Intel Corporation.
* 
* SPDX-License-Identifier: BSD-3-Clause
'''

import sys
import os
import connexion
import json
import asyncio
from openapi_server import encoder

sys.path.append(os.path.dirname(__file__) + "/../../")
from common import settings
from modules.PipelineManager import PipelineManager
from modules.ModelManager import ModelManager
from threading import Thread

from common.utils import logging

from optparse import OptionParser

logger = logging.get_logger('main', is_static=True)

def get_options():
    parser = OptionParser()
    parser.add_option("-p", "--port", action="store", type="int", dest="port", default=int(os.getenv('PORT','8080')))
    parser.add_option("--framework", action="store", dest="framework",
                      choices=['gstreamer', 'ffmpeg'], default=os.getenv('FRAMEWORK','gstreamer'))
    parser.add_option("--pipeline_dir", action="store", dest="pipeline_dir",
                      type="string", default=os.getenv("PIPELINE_DIR",'pipelines'))
    parser.add_option("--model_dir", action="store", dest="model_dir",
                      type="string", default=os.getenv("MODEL_DIR",'models'))
    parser.add_option("--network_preference", action="store", 
                      dest="network_preference",
                      type="string", default=os.getenv('NETWORK_PREFERENCE', '{}'))
    parser.add_option("--max_running_pipelines", action="store", 
                      dest="max_running_pipelines",
                      type="int", default=int(os.getenv('MAX_RUNNING_PIPELINES', '1')))
    parser.add_option("--log_level", action="store", 
                      dest="log_level",
                      choices=['INFO','DEBUG'], default=os.getenv('LOG_LEVEL', 'INFO'))
    parser.add_option("--config_path", action="store", 
                      dest="config_path",
                      default=os.getenv('CONFIG_PATH', os.path.dirname(__file__) + "/../../../"))
    

    return parser.parse_args()


def gobject_mainloop():
    import gi
    gi.require_version('Gst', '1.0')
    from gi.repository import Gst, GObject
    mainloop = GObject.MainLoop()
    try:
        mainloop.run()
    except KeyboardInterrupt:
        pass

def parse_network_preference(options):
    try:
        return json.loads(options.network_preference)
    except Exception as error:
        logger.warning("Invalid network preference: %s" %(error,))
        return {}

def main(options):
    
    PipelineManager.load_config(os.path.join(options.config_path, options.pipeline_dir), options.max_running_pipelines)
    ModelManager.load_config(os.path.join(options.config_path, options.model_dir),parse_network_preference(options))
    app = connexion.App(__name__, specification_dir='./openapi/')
    app.app.json_encoder = encoder.JSONEncoder
    app.add_api('openapi.yaml', arguments={'title': 'Video Analytics Serving API'})
    logger.info("Starting Tornado Server on port: {p}".format(p=options.port))
    app.run(server='tornado', port=options.port)


if __name__ == '__main__':

    try:
        options, args = get_options()
        settings.set_log_level(options.log_level)
    except Exception as error:
        print(error)
        logger.error("Getopt Error!")
        exit(1)

    thread = Thread(target=main, args=[options])
    thread.daemon = True
    thread.start()

    if (options.framework == "gstreamer"):
        gobject_mainloop()
    else:
        thread.join()

    logger.info("Exiting")
