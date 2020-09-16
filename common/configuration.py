#!/usr/bin/python3

import os

env=dict(os.environ)
try:
    with open(env["CONFIG_FILE"],"rt") as fd:
        import json
        env.update(json.load(fd))
except:
    pass
