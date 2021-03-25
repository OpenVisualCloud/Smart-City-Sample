#!/bin/bash -e

DIR=$(dirname $(readlink -f "$0"))

# create sensor-info.m4
if [[ ! -f "$DIR/sensor-info.m4" ]] || [[ "$DIR/sensor-info.json" -nt "$DIR/sensor-info.m4" ]]; then
    cat > "$DIR/mkm4.py" <<EOF
import json
import sys

data={}
with open(sys.argv[1],"rt") as fd:
    for s1 in json.load(fd):
        name=s1["scenario"]
        if name not in data: data[name]=[]
        data[name].append(s1["location"])

print("define(\`SCENARIOS',\`{}')dnl".format(" ".join(data.keys())))
for s1 in data:
    oi=1
    for o1 in data[s1]:
        print("define(\`{}_office{}_location',\`{},{}')dnl".format(s1,oi,o1["lat"],o1["lon"]))
        oi=oi+1
EOF

    docker run --rm -v "$DIR:/home:ro" -it centos:7 python /home/mkm4.py /home/sensor-info.json > "$DIR/sensor-info.m4"
    rm -f "$DIR/mkm4.py"
fi

