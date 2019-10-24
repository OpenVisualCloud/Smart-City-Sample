'''
* Copyright (C) 2019 Intel Corporation.
* 
* SPDX-License-Identifier: BSD-3-Clause
'''

from ctypes import *  # pylint: disable=unused-wildcard-import

clib = CDLL("/usr/lib/x86_64-linux-gnu/gstreamer-1.0/libgstvideoanalyticsmeta.so")

# json meta

clib.get_json_message.argtypes = [c_void_p]
clib.get_json_message.restype = c_char_p


def get_json_message(meta):
    return clib.get_json_message(hash(meta))
