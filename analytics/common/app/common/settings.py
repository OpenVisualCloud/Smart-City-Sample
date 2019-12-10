'''
* Copyright (C) 2019 Intel Corporation.
*
* SPDX-License-Identifier: BSD-3-Clause
'''

"""
    define logging settings here
"""

import os

LOG_LEVEL = "INFO"
LOG_ATTRS = ['levelname', 'asctime', 'message', 'name']

def set_log_level(level):
    global LOG_LEVEL
    LOG_LEVEL = level
