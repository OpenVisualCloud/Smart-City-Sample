'''
* Copyright (C) 2019 Intel Corporation.
* 
* SPDX-License-Identifier: BSD-3-Clause
'''

tags = {
    "type": "object",
    "element": {
        "name": "metaconvert",
        "property": "tags",
        "format": "json"
    }
}


source = {
    "uri": {
        "type":"object",
        "properties": {
            "type": {
                "type":"string",
                "enum":["uri"]
            },
            "uri": {
                "type":"string",
                "format":"uri",
                "element":[{"name":"source",
                            "property":"uri"},
                           {"name":"source",
                            "property":"location"},
                           {"name":"metaconvert","property":"source"}]}
        },
        "required":["type","uri"]
    },
    "device": {
        "type":"object",
        "properties": {
            "type":{"type":"string","enum":["device"]},
            "path":{"type":"string","format":"path","element":[{"name":"source","property":"device"},
                                                               {"name":"metaconvert","property":"source"}]}
        },
        "required":["type","path"]
    },
    "oneOf": [
        {
            "$ref": "#/uri"
        },
        {
            "$ref": "#/device"
        }
    ]
}

destination = {
    "file": {
      "type": "object",
      "properties": {
        "type": {
          "type": "string",
          "enum": ["file"],
          "element": {
            "name": "destination",
            "property": "method"
          }
        },
        "path": {
          "type": "string",
          "format": "path",
          "element": {
            "name": "destination",
            "property": "filepath"
          }
        },
        "format": {
          "type": "string",
          "enum": [
            "stream",
            "batch"
          ],
          "element": {
            "name": "destination",
            "property": "outputformat"
          }
        }
      },
        "required":["type","path"]
    },
    "mqtt": {
      "type": "object",
      "properties": {
        "type": {
            "type": "string",
            "enum": ["mqtt"],
            "element":{"name":"destination","property":"method"}
        },
        "host": {
          "type": "string",
          "element": {
            "name": "destination",
            "property": "address"
          }
        },
        "topic": {
          "type": "string",
          "element": "destination"
        },
        "clientId": {
          "type": "string",
          "element": "destination"
        },
        "timeout": {
          "type": "integer",
          "element": "destination"
        }
      },
    "required": [
          "host",
          "type",
          "topic"
      ]
    },
    "kafka": {
      "type": "object",
      "properties": {
        "type": {
          "type": "string",
          "enum": ["kafka"],
            "element":{"name":"destination","property":"method"}
        },
        "host": {
          "type": "string",
          "description": "host:port to use as bootstrap server.",
          "element": {
            "name": "destination",
            "property": "address"
          }
        },
        "topic": {
          "type": "string",
            "element": "destination"
        }
      },
      "required": [
          "type",
          "host",
          "topic"
      ]
    },
  "oneOf": [
    {
      "$ref": "#/kafka"
    },
    {
      "$ref": "#/mqtt"
    },
    {
      "$ref": "#/file"
    }
  ]
}

