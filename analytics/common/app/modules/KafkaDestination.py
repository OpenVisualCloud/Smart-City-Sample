'''
* Copyright (C) 2019 Intel Corporation.
* 
* SPDX-License-Identifier: BSD-3-Clause
'''

from modules.Destination import Destination  # pylint: disable=import-error
from kafka import KafkaProducer  # pylint: disable=import-error
from kafka.client import KafkaClient  # pylint: disable=import-error
import json


class KafkaDestination(Destination):

    def __init__(self, destination):

        try:
            self.topic = destination["topic"]
            
            self.producer = KafkaProducer(bootstrap_servers=destination["hosts"],
                                          api_version=(0, 10),
                                          value_serializer=lambda m: json.dumps(m).encode('ascii'))
        except Exception as error:
            self.producer = None
            raise error
    
    def send(self, result):
        self.producer.send(self.topic, result)
