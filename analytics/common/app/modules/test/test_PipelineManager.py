import sys, os
sys.path.append(os.path.normpath(os.path.join(os.path.dirname(__file__), "..", "..")))

import unittest
import common

from modules.PipelineManager import PipelineManager

class TestPipelineManager(unittest.TestCase):
    """
    Test GetLoadedPipelines
    """

    def test_get_pipeline_parameters(self):

        PipelineManager.pipelines = {
            "object_detection": {
                1: {
                    "name": "object_detection",
                    "version": 1,
                    "type": "GStreamer",
                    "template": "",
                    "description": "Object Detection Pipeline",
                    "parameters": {
                        "send-empty": {
                            "element":"jsonmetaconvert"
                        },
                        "every-nth-frame": {
                            "element":"detection"
                        }
                    }
                }
            }
        }

        expected_result = {
            "name": "object_detection",
            "version": 1,
            "type": "GStreamer",
            "description": "Object Detection Pipeline",
            "parameters": {
                "send-empty": {
                    "element":"jsonmetaconvert"
                },
                "every-nth-frame": {
                    "element":"detection"
                }
            }
        }
        result = PipelineManager.get_pipeline_parameters("object_detection", 1)

        self.assertEqual(result, expected_result)

    def test_get_loaded_pipelines_empty(self):
        
        PipelineManager.pipelines = None

        expected_result = []
        result = PipelineManager.get_loaded_pipelines()
                
        self.assertEqual(result, expected_result)

    def test_get_loaded_pipelines_populated(self):

        PipelineManager.pipelines = {
            "object_detection": {
                1: {
                    "name": "object_detection",
                    "version": 1,
                    "type": "GStreamer",
                    "template": "",
                    "description": "Object Detection Pipeline",
                    "parameters": {
                        "send-empty": {
                            "element":"jsonmetaconvert"
                        },
                        "every-nth-frame": {
                            "element":"detection"
                        }
                    }
                }
            }
        }

        expected_result = [{
            "name": "object_detection",
            "version": 1,
            "type": "GStreamer",
            "description": "Object Detection Pipeline",
            "parameters": {
                "send-empty": {
                    "element":"jsonmetaconvert"
                },
                "every-nth-frame": {
                    "element":"detection"
                }
            }
        }]
        result = PipelineManager.get_loaded_pipelines()

        self.assertEqual(result, expected_result)

    def test_create_instance(self):
        mock_pipeline = type("MockPipeline", (object,), dict(start=lambda : "started"))
        PipelineManager.pipeline_types = {
            "GStreamer": lambda id, config, models, request: mock_pipeline
        }

        PipelineManager.pipelines = {
            "object_detection": {
                "1": {
                    "name": "object_detection",
                    "version": 1,
                    "type": "GStreamer",
                    "template": "",
                    "description": "Object Detection Pipeline",
                    "parameters": {
                        "send-empty": {
                            "element":"jsonmetaconvert"
                        },
                        "every-nth-frame": {
                            "element":"detection"
                        }
                    }
                }
            }
        }

        request_to_send = {
            'source': {
                'uri': 'path_to_source', 
                'type': 'uri'
            }, 
            'destination': {
                'uri': 'path_to_destination', 
                'type': 'file'
            }
        }
        expected_result = 1
        result = PipelineManager.create_instance("object_detection", 1, request_to_send)

        self.assertEqual(result, expected_result)

    def test_load_config(self):

        PipelineManager.pipeline_types = {
            "GStreamer": "DummyType"
        }
        
        expected_result = {
            'gstreamer': {
                'object_detection': {}
            },
            'object_detection': {
                '1': {
                    "name": "object_detection",
                    "version": 1,
                    "type": "GStreamer",
                    "description": "Object Detection Pipeline"
                }
            }
        }

        expected_max_running_pipelines = 3
        PipelineManager.load_config(os.path.join(os.path.dirname(__file__),"pipelines"), expected_max_running_pipelines)
        result = PipelineManager.pipelines
        result_max_running_pipelines = PipelineManager.MAX_RUNNING_PIPELINES

        self.assertEqual(result, expected_result)
        self.assertEqual(result_max_running_pipelines, expected_max_running_pipelines)

    def test_get_instance_parameters(self):

        PipelineManager.pipeline_instances = {
            1: type('GstreamerPipeline', (object,), {
                "params": lambda self: {
                    "id": 1,
                    "request": None,
                    "type": "gstreamer",
                    "launch_command": None
                }
            })()
        }

        expected_result = {
            "id": 1,
            "request": None,
            "type": "gstreamer",
            "launch_command": None
        }
        result = PipelineManager.get_instance_parameters(1)

        self.assertEqual(result, expected_result)

    def test_get_instance_status(self):
        PipelineManager.pipeline_instances = {
            1: type('GstreamerPipeline', (object,), {
                "status": lambda self: {
                    "id": 1,
                    "state": "RUNNING",
                    "avg_fps": 100000,
                    "start_time": 1234,
                    "elapsed_time": 1234
                }
            })()
        }

        expected_result = {
            "id": 1,
            "state": "RUNNING",
            "avg_fps": 100000,
            "start_time": 1234,
            "elapsed_time": 1234
        }
        result = PipelineManager.get_instance_status(1)

        self.assertEqual(result, expected_result)

    def test_stop_instance(self):
        PipelineManager.pipeline_instances = {
            1: type('GstreamerPipeline', (object,), {
                "stop": lambda self: {
                    "id": 1,
                    "state": "RUNNING",
                    "avg_fps": 100000,
                    "start_time": 1234,
                    "elapsed_time": 1234
                }
            })()
        }

        expected_result = {
            "id": 1,
            "state": "RUNNING",
            "avg_fps": 100000,
            "start_time": 1234,
            "elapsed_time": 1234
        }
        result = PipelineManager.stop_instance(1)

        self.assertEqual(result, expected_result)

if __name__ == '__main__':
    unittest.main()

