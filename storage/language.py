#!/usr/bin/python3

from urllib.parse import quote

text={
    "cleanup": "cleanup",
    "maintenance": "maintenance",
    "halt recording": "Halt recording: {}%",
    "disk usage": "Disk usage: {}%",
    "connection error": "Connection Error",
}

def encode(msg):
    return quote(str(msg))


