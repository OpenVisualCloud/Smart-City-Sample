import sys, os
sys.path.append(os.path.normpath(os.path.join(os.path.dirname(__file__), "..", "..")))

import unittest
from unittest.mock import patch
import common

MockDestination = MagicMock()
MockDestination.import_destination_types.return_type = "1234"
MockDestination.Destination = 

class TestFileDestination(unittest.TestCase):

    @patch('modules.FileDestination.urllib.parse.urlparse')
    @patch('modules.FileDestination.os.path.abspath')
    @patch('modules.FileDestination.os.path.dirname')
    @patch('modules.FileDestination.os.makedirs', return_value = None)
    @patch('modules.FileDestination.open')
    def test__init(self, mock_open, mock_makedirs, mock_dirname, mock_abspath, mock_urlparse):

        mock_urlparse.return_value = {
            "scheme": "file",
            "path": "/root/test"
        }
        mock_abspath.return_value = "/root/test"
        mock_dirname.return_value = "/root/"
        mock_open.return_value = "destinationfile"

        testfiledestination = FileDestination({
            "uri": "file:///root/test"
        })

        self.assertEqual(self.uri.path, "/root/test")
        self.assertEqual(self.uri.scheme, "file")
        self.assertEqual(self.destination_path, "/root/test")
        self.assertEqual(self.destination, "destinationfile")
        mock_urlparse.assert_called_with("file:///root/test")
        mock_abspath.assert_called_with("/root/test")
        mock_dirname.assert_called_with("/root/test", True)
        mock_open.assert_called_with("/root/test", 'w')

if __name__ == '__main__':
    unittest.main()
