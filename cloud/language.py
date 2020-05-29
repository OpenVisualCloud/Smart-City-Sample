#!/usr/bin/python3

from urllib.parse import quote

text={
    "connection error": "Connection Error",
}

def encode(msg):
    return quote(str(msg))

