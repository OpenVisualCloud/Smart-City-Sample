import sys, os
sys.path.append(os.path.normpath(os.path.join(os.path.dirname(__file__), "..", "..")))

import unittest
from unittest.mock import patch

with patch('modules.Destination.import_destination_types', return_value=1234):
    with patch('')
    from modules.GStreamerPipeline import GStreamerPipeline
