"""
    define service level settings for Video Analytics Service here
"""

import os

CONFIG_PATH = os.path.dirname(__file__) + "/../../"
MAX_RUNNING_PIPELINES = -1

LOG_LEVEL = "DEBUG"
LOG_ATTRS = ['levelname', 'asctime', 'message', 'name']
