#!/usr/bin/python3

from base64 import b64encode

text={
    "connection error": "Connection Error",
}

def encode(msg):
    return str(msg).encode('base64')

