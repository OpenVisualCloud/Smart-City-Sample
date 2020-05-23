# smtc_analytics_object_xeon_gst

FROM smtc_analytics_common_xeon_gst

RUN  apt-get update -qq && apt-get install -qq python3-paho-mqtt python3-ply python3-requests python3-watchdog && rm -rf /var/lib/apt/lists/*

COPY --from=smtc_common /home/*.py /home/
COPY *.py /home/
COPY models /home/models
COPY Xeon/gst/pipeline /home/pipelines/object_detection
CMD ["/home/detect-object.py"]

####
ARG  USER=docker
ARG  GROUP=docker
ARG  UID
ARG  GID
## must use ; here to ignore user exist status code
RUN  [ ${GID} -gt 0 ] && groupadd -f -g ${GID} ${GROUP}; \
     [ ${UID} -gt 0 ] && useradd -d /home/${USER} -g ${GID} -K UID_MAX=${UID} -K UID_MIN=${UID} ${USER}; \
     chown -R ${UID}:${GID} /home
USER ${UID}
####
