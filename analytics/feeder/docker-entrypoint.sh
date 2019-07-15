#!/bin/bash -e
ERRCODE=0
echo "Starting container..."
echo "Setting VA debug level to INFO"
sed -i "s/DEBUG/INFO/" /home/video-analytics/app/common/settings.py
command1='echo "starting video analytics service"; cd video-analytics/app/server; python3 -m openapi_server $@ &'
command2='echo "starting feeder"; cd ../../..; python3 main.py &'

commands=(
    "{ $command1 }"
    "{ $command2 }"
)
numcmds=`expr "${#commands[@]}" - 1`
for i in `seq 0 "$numcmds"`; do
    echo "Launching Command# $i in background..."
    eval "${commands[$i]} ;"
    echo "Command# ${i} running as PID# ${!}"
done

# await exit from any launched process
wait -n

ERRCODE=$?
echo $ERRCODE
if [ "$ERRCODE" == "0" ];
then
echo "Closed Container Successfully"
else
echo "Fatal Exit! ($ERRCODE)"
fi
# signal all members in this process group
kill 0
