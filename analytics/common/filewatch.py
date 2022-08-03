#!/usr/bin/python3


import json
import time
import socket
from threading import Thread, Event


WATCHER_POLL_TIME = 0.01

class FileWatcher():

    def __init__(self, filename, sleep_time=WATCHER_POLL_TIME):
        super().__init__()
        self.filename = filename
        self.sleep_time = sleep_time
        self.watcher_thread = None
        self.trigger_stop = False
        self.result_watcher = None
        self._started_event = Event()
        self.watcher_thread = Thread(target=self._watch_method)

    def start(self, result_watcher):
        self.result_watcher = result_watcher
        self.watcher_thread.start()
        self._started_event.wait()

    def stop(self):
        if self._watching:
            self.trigger_stop = True
            self.watcher_thread.join()

    def _watch_method(self):
        try:
            with open(self.filename, 'r') as file:
                self._watching = True
                self._started_event.set()
                while not self.trigger_stop:
                    where = file.tell()
                    line = file.readline()
                    if not line:
                        time.sleep(self.sleep_time)
                        file.seek(where)
                    else:
                        try:
                            self.result_watcher.results_cb(line)
                        except ValueError:
                            pass
            self._watching = False
        except OSError:
            self.error_message = "Unable to read from file {}".format(self.filename)
            self._started_event.set()
