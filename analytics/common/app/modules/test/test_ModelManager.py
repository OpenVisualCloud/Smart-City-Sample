import sys, os
sys.path.append(os.path.normpath(os.path.join(os.path.dirname(__file__), "..", "..")))

import unittest
import common

from modules.ModelManager import ModelManager

class TestModelManager(unittest.TestCase):

    def test_get_loaded_models_empty(self):
        
        ModelManager.models = None

        expected_result = []
        result = ModelManager.get_loaded_models()

        self.assertEqual(result, expected_result)

    def test_load_config(self):
        ModelManager.load_config("../models")

        print(ModelManager.models)

if __name__ == '__main__':
    unittest.main()

