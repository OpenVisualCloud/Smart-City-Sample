#!/bin/bash -e

DIR=$(dirname $(readlink -f "$0"))
NOFFICES="${4:-1}"
NCAMERAS="${5:-5}"

for ((OFFICE=1;OFFICE<=${NOFFICES};OFFICE++)); do
    RTSP_PORT=$((16000+${OFFICE}*1000))
    RTP_PORT=$((26000+${OFFICE}*1000))
    echo sudo -E docker run -e 'FILES=.mp4$$' -e "NCAMERAS=${NCAMERAS}" -e "RTSP_PORT=$RTSP_PORT" -e "RTP_PORT=$RTP_PORT" -e "PORT_STEP=10" --network=host --name=opncam_office${OFFICE} --rm -i smtc_sensor_simulation:latest
    sudo -E docker run -e 'FILES=.mp4$$' -e "NCAMERAS=${NCAMERAS}" -e "RTSP_PORT=$RTSP_PORT" -e "RTP_PORT=$RTP_PORT" -e "PORT_STEP=10" --network=host --name=opncam_office${OFFICE} --rm -i smtc_sensor_simulation:latest 2> /dev/null &
done

