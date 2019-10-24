'''
* Copyright (C) 2019 Intel Corporation.
* 
* SPDX-License-Identifier: BSD-3-Clause
'''

import os
from modules.Destination import Destination  # pylint: disable=import-error
import urllib
import json


class FileDestination(Destination):

    def __init__(self, destination):
        self.destination = None

        try:
            self.uri = urllib.parse.urlparse(destination["uri"])
            if self.uri.scheme != "file":
                raise Exception("Invalid scheme for file destination")

            self.destination_path = os.path.abspath(self.uri.path)
            os.makedirs(os.path.dirname(self.destination_path),exist_ok=True)
            self.destination = open(self.destination_path,'w')
        except Exception as error:
            self.destination=None
            raise(error)
    
    def send(self,result):
        if (self.destination):
            self.destination.write(json.dumps(result)+"\n")
            
            
    def __del__(self):
        if (self.destination):
            self.destination.flush()
            self.destination.close()

    
