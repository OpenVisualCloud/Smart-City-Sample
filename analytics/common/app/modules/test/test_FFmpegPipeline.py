import sys, os
sys.path.append(os.path.normpath(os.path.join(os.path.dirname(__file__), "..", "..")))

import unittest
from unittest.mock import patch
import common

with patch('shutil.which', return_value="1234"):
    from modules.FFmpegPipeline import FFmpegPipeline

MockProcess = type("MockProcess", (object,), {
    "kill": lambda: None,
    "wait": lambda self: None,
    "returncode": 0,
    "poll": lambda self: None
})

class TestFFmpegPipeline(unittest.TestCase):

    def test_init(self):
        result = FFmpegPipeline(1, {"template": None}, "models")
        
        self.assertIsInstance(result, FFmpegPipeline)
        self.assertEqual(result.config, {"template": None})
        self.assertEqual(result.models, "models")
        self.assertEqual(result.id, 1)
        self.assertEqual(result.template, None)
    
    def test_stop(self):
        testpipeline = FFmpegPipeline(1, {"template": None}, "models")
        testpipeline._process = MockProcess

        testpipeline.stop()

        self.assertEqual(testpipeline.state, "ABORTED")

    def test_params(self):
        testpipeline = FFmpegPipeline(1, {"template": None, "type": "ffmpeg"}, "models")
        testpipeline.request = {
            "models": "dummymodels"
        }
        testpipeline._ffmpeg_launch_string = "dummylaunchstring"

        expected_result = {
            "id": 1, 
            "request": {}, 
            "type": "ffmpeg", 
            "launch_command": "dummylaunchstring"
        }
        result = testpipeline.params()

        self.assertEqual(result, expected_result)

    @patch('modules.FFmpegPipeline.time.time', return_value = 1001)
    def test_status_running(self, mocktime):
        testpipeline = FFmpegPipeline(1, {"template": None, "type": "ffmpeg"}, "models")
        testpipeline.state = "RUNNING"
        testpipeline.start_time = 1000
        testpipeline.fps = 10

        expected_result = {
            "id": 1,
            "state": "RUNNING",
            "avg_fps": 10,
            "start_time": 1000,
            "elapsed_time": 1
        }
        result = testpipeline.status()

        self.assertEqual(result, expected_result)

    def test_status_stopped(self):
        testpipeline = FFmpegPipeline(1, {"template": None, "type": "ffmpeg"}, "models")
        testpipeline.state = "COMPLETED"
        testpipeline.start_time = 1000
        testpipeline.stop_time = 1001
        testpipeline.fps = 10

        expected_result = {
            "id": 1,
            "state": "COMPLETED",
            "avg_fps": 10,
            "start_time": 1000,
            "elapsed_time": 1
        }
        result = testpipeline.status()

        self.assertEqual(result, expected_result)

    @patch('modules.FFmpegPipeline.time.time', return_value=1001)
    @patch('modules.FFmpegPipeline.subprocess.Popen', return_value=MockProcess())
    def test__spawn_run_completed_successfully(self, mockpopen, mocktime):
        testpipeline = FFmpegPipeline(1, {"template": None, "type": "ffmpeg"}, "models")
        args = "TESTARGS"

        testpipeline._spawn(args)

        mockpopen.assert_called_with(args, bufsize=1, stderr=-1, stdout=-1, universal_newlines=True)
        self.assertEqual(testpipeline.start_time, 1001)
        self.assertEqual(testpipeline.stop_time, 1001)
        self.assertEqual(testpipeline.state, "COMPLETED")
        self.assertEqual(testpipeline._process, None)
    
    @patch('modules.FFmpegPipeline.time.time', return_value=1001)
    @patch('modules.FFmpegPipeline.subprocess.Popen', return_value=type("MockProcess", (object,), {
        "kill": lambda: None,
        "wait": lambda self: None,
        "returncode": 1,
        "poll": lambda self: None
    })())
    def test__spawn_run_completed_error(self, mockpopen, mocktime):
        testpipeline = FFmpegPipeline(1, {"template": None, "type": "ffmpeg"}, "models")
        args = "TESTARGS"

        testpipeline._spawn(args)

        mockpopen.assert_called_with(args, bufsize=1, stderr=-1, stdout=-1, universal_newlines=True)
        self.assertEqual(testpipeline.start_time, 1001)
        self.assertEqual(testpipeline.stop_time, 1001)
        self.assertEqual(testpipeline.state, "ERROR")
        self.assertEqual(testpipeline._process, None)

    def test__add_tags_empty(self):
        testpipeline = FFmpegPipeline(1, {"template": None, "type": "ffmpeg"}, "models")
        testpipeline.request = {}
        iemetadata_args = []
    
        testpipeline._add_tags(iemetadata_args)

        self.assertEqual(iemetadata_args, [])

    def test__add_tags(self):
        testpipeline = FFmpegPipeline(1, {"template": None, "type": "ffmpeg"}, "models")
        testpipeline.request = {
            "tags": {
                "tag1": "value1",
                "tag2": "value2"
            }
        }
        iemetadata_args = []

        testpipeline._add_tags(iemetadata_args)

        self.assertEqual(str(iemetadata_args).count('-custom_tag'), 2)
        self.assertRegex(str(iemetadata_args), "tag.:value.,")
        self.assertRegex(str(iemetadata_args), "tag.:value.\'")
        self.assertIn('tag1:value1', str(iemetadata_args))
        self.assertIn('tag2:value2', str(iemetadata_args))

    @patch('modules.FFmpegPipeline.logger.error', return_value=None)
    def test__add_tags_error(self, mock_log_error):
        testpipeline = FFmpegPipeline(1, {"template": None, "type": "ffmpeg"}, "models")
        testpipeline.request = {
            "tags": {
                "tag1": "value1",
                "tag2": "value2"
            }
        }
        expected_iemetadata_args = ['-custom_tag', 'tag1:value1,', '-custom_tag', 'tag2:value2']

        testpipeline._add_tags(None)

        mock_log_error.assert_called_with("Error adding tags")

    def test__add_default_parameters(self):
        testpipeline = FFmpegPipeline(1, {"template": None, "type": "ffmpeg"}, "models")

        testpipeline.config = {
            "parameters": {
                "param1": {
                    "default": 1234
                },
                "param2": {},
                "param3": {
                    "default": 1234
                }
            }
        }
        testpipeline.request = {
            "parameters": {
                "param3": {},
                "param4": {}
            }
        }
        expected_result = {
            "parameters": {
                'param3': {}, 
                'param4': {}, 
                'param1': 1234
            }
        }

        testpipeline._add_default_parameters()

        self.assertEqual(testpipeline.request, expected_result)

    @patch('modules.FFmpegPipeline.logger.debug', return_value=None)
    @patch('modules.FFmpegPipeline.Thread')
    def test_start(self, mock_thread, mock_log_debug):
        pass
        config = {
            "template": "uri=\"{source[uri]}\"", 
            "type": "ffmpeg",
            "parameters": {
                "param1": {
                    "default": 1234
                },
                "param2": {},
                "param3": {
                    "default": 1234
                }
            }
        }

        testpipeline = FFmpegPipeline(1, config, "models")

        request = {
            "source": {
                "uri": "testuri"
            },
            "destination": {
                "hosts": ["host1"],
                "type": "kafka",
                "topic": "testtopic",
                "uri": "testuri"
            }
        }

        testpipeline.start(request)
        mock_log_debug.assert_called_with(['ffmpeg', 'uri=testuri', '-f', 'iemetadata', '-source_url', 'testuri', 'kafka://host1/testtopic'])

if __name__ == '__main__':
    unittest.main()

