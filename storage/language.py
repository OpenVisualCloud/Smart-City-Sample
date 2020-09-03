#!/usr/bin/python3

from urllib.parse import quote

text={
    "cleanup": "清扫服务",
    "maintenance": "维护服务",
    "halt recording": "停止录影: 磁盘{}%",
    "disk usage": "磁盘使用: {}%",
    "connection error": "链接错误",
}

def encode(msg):
    return quote(str(msg))


