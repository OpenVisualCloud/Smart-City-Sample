#!/bin/bash -e

(cat | /usr/bin/python3 - >/tmp/env.conf) <<EOF
from configuration import env
print("\\n".join([k+'="'+env[k]+'"' for k in env if k.startswith("$1")]))
EOF

. /tmp/env.conf
