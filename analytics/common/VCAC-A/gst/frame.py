# ==============================================================================
# Copyright (C) 2018-2019 Intel Corporation
#
# SPDX-License-Identifier: MIT
# ==============================================================================

from .videoregionofinterestmeta import VideoRegionOfInterestMeta
from . import util as util
from .tensormeta import TensorMeta
from .jsonmeta import JSONMeta

from contextlib import contextmanager
import gi

gi.require_version('Gst', '1.0')
gi.require_version("GstVideo", "1.0")
gi.require_version("GLib", "2.0")

from gi.repository import Gst, GstVideo, GLib
import numpy


class VideoFrame:

    FORMAT_CHANNELS = {'BGRx': 4,
                       'BGRA': 4,
                       'RGB': 3,
                       'BGR': 3,
                       'NV12':3}

    def __init__(self, buffer, caps=None):
        self.buffer = buffer
        self.caps = caps
        self.caps_str = self.caps.get_structure(0)
        self.video_meta = GstVideo.buffer_get_video_meta(buffer)
        if (not self.video_meta):
            self.video_meta = GstVideo.VideoInfo()
            self.video_meta.from_caps(self.caps)
        self.width = self.video_meta.width
        self.height = self.video_meta.height
        self.format_str = self.caps_str.get_string("format")
        self.channels = VideoFrame.FORMAT_CHANNELS[self.format_str]

    @contextmanager
    def data(self, flags=Gst.MapFlags.WRITE):
        with util.gst_buffer_data(self.buffer, flags) as data:
            try:
                yield numpy.ndarray((self.height, self.width, self.channels),
                                    buffer=data,
                                    dtype=numpy.uint8)
            finally:
                pass

    def regions(self):
        return VideoRegionOfInterestMeta.iterate(self.buffer)

    def tensors(self):
        return TensorMeta.iterate(self.buffer)

    def messages(self):
        return JSONMeta.iterate(self.buffer)

    def add_region(self, label, x, y, width, height):
        return VideoRegionOfInterestMeta.add_video_region_of_interest_meta(self.buffer,
                                                                           label,
                                                                           x,
                                                                           y,
                                                                           width,
                                                                           height)

    def remove_region(self, detection):
        return VideoRegionOfInterestMeta.remove_video_region_of_interest_meta(self.buffer, detection)

    def add_message(self, message):
        return JSONMeta.add_json_meta(self.buffer, message)

    def remove_message(self, message):
        return JSONMeta.remove_json_meta(self.buffer, message)

    def add_tensor(self, precision, rank, dims, layout, layer_name, model_name, data, total_bytes, element_id):
        return TensorMeta.add_tensor_meta(self.buffer,
                                          precision,
                                          rank,
                                          dims,
                                          layout,
                                          layer_name,
                                          model_name,
                                          data,
                                          total_bytes,
                                          element_id)

    def remove_tensor(self, tensor):
        return TensorMeta.remove_tensor_meta(self.buffer, tensor)


class AudioFrame:
    FORMAT_TYPE = {'S16LE': numpy.int16}

    def __init__(self, buffer, caps):
        self.buffer = buffer
        self.caps = caps
        self.caps_struct = self.caps.get_structure(0)
        self.rate = self.caps_struct.get_int("rate").value
        self.channels = self.caps_struct.get_int("channels").value
        self.format_string = self.caps_struct.get_string("format")
        self.layout = self.caps_struct.get_string("layout")

    @contextmanager
    def data(self, flags=Gst.MapFlags.WRITE):
        with util.gst_buffer_data(self.buffer, flags) as data:
            try:
                yield numpy.frombuffer(buffer=data, dtype=AudioFrame.FORMAT_TYPE[self.format_string])
            finally:
                pass

    def messages(self):
        return [x for x in JSONMeta.iterate(self.buffer)]

    def add_message(self, message):
        return JSONMeta.add_json_meta(self.buffer, message)

    def remove_message(self, message):
        return JSONMeta.remove_json_meta(self.buffer, message)


def from_sample(sample):
    buffer = sample.get_buffer()
    caps = sample.get_caps()
    return Frame(caps, buffer)


@contextmanager
def from_info(pad, info):
    caps = pad.get_current_caps()
    with util.GST_PAD_PROBE_INFO_BUFFER(info) as buffer:
        try:
            yield Frame(caps, buffer)
        finally:
            pass


def Frame(buffer, caps):
    caps_structure = caps.get_structure(0)
    caps_string = GLib.quark_to_string(caps_structure.name)
    if ("video" in caps_string):
        return VideoFrame(buffer, caps)
    elif ("audio" in caps_string):
        return AudioFrame(buffer, caps)
