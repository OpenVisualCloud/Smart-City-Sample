#!/usr/bin/python3

from urllib.parse import quote

text={
    "connection error": "链接错误",
}

def encode(msg):
    return quote(str(msg))

