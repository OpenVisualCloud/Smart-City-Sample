import sys, os
sys.path.append(os.path.normpath(os.path.join(os.path.dirname(__file__), "..", "..")))

import unittest
import common
from common.utils import logging  # pylint: disable=import-error

import modules.Destination as Destination
from contextlib import contextmanager
from io import StringIO

class TestDestination(unittest.TestCase):

    def test_create_instance_kafka(self):
        request = {
            "destination": {
                "type": "kafka"
            }
        }
        MockKafkaDestination = type("MockKafkaDestination", (object,), {
            "__init__": lambda self, destination: None
        })
        Destination.destination_types['kafka'] = MockKafkaDestination

        result = Destination.create_instance(request)

        self.assertIsInstance(result, MockKafkaDestination)

    def test_create_instance_bad_type(self):
        request = {
            "destination": {
                "type": "test"
            }
        }
        MockKafkaDestination = type("MockKafkaDestination", (object,), {
            "__init__": lambda self, destination: None
        })
        Destination.destination_types['kafka'] = MockKafkaDestination
        logger = logging.get_logger('DestinationTypes', is_static=True)

        with self.assertLogs(logger=logger,level='DEBUG') as cm:
            result = Destination.create_instance(request)
        self.assertIn("Error", cm.output.pop())

    def test_create_instance_empty_request(self):
        request = None
        MockKafkaDestination = type("MockKafkaDestination", (object,), {
            "__init__": lambda self, destination: None
        })
        Destination.destination_types['kafka'] = MockKafkaDestination
        logger = logging.get_logger('DestinationTypes', is_static=True)

        with self.assertLogs(logger=logger,level='DEBUG') as cm:
            result = Destination.create_instance(request)
        self.assertIn("Error", cm.output.pop())

if __name__ == '__main__':
    unittest.main()
