
FROM video_analytics_service_gstreamer

USER root
RUN  apt-get update && apt-get install -y ffmpeg python3-paho-mqtt python3-ply python3-requests python3-watchdog
RUN  rm -r /home/video-analytics/models && rm -r /home/video-analytics/pipelines

COPY *.py /home/
COPY models /home/video-analytics/models
COPY pipelines/gstreamer /home/video-analytics/pipelines
ENTRYPOINT ["/home/main.py"]

####
ARG  USER
ARG  GROUP
ARG  UID
ARG  GID
## must use ; here to ignore user exist status code
RUN  groupadd -f -g ${GID} ${GROUP};useradd -d /home/${USER} -g ${GROUP} -K UID_MAX=${UID} -K UID_MIN=${UID} ${USER};echo
USER ${USER}
####
