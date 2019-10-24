import unittest

from test_PipelineManager import TestPipelineManager
from test_ModelManager import TestModelManager
from test_Destination import TestDestination
from test_FFmpegPipeline import TestFFmpegPipeline

def my_suite():
    suite = unittest.TestSuite()
    result = unittest.TestResult()
    suite.addTest(unittest.makeSuite(TestPipelineManager))
    suite.addTest(unittest.makeSuite(TestModelManager))
    suite.addTest(unittest.makeSuite(TestDestination))
    suite.addTest(unittest.makeSuite(TestFFmpegPipeline))
    runner = unittest.TextTestRunner()
    print(runner.run(suite))

my_suite()