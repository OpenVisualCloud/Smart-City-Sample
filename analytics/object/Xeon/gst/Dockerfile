# smtc_analytics_object_xeon_gst

FROM smtc_analytics_common_xeon_gst

RUN  apt-get update -qq && apt-get install -qq python3-paho-mqtt python3-ply python3-requests python3-watchdog && rm -rf /var/lib/apt/lists/*

COPY --from=smtc_common /home/*.py /home/
COPY *.py /home/
COPY models /home/models
COPY Xeon/gst/pipeline /home/pipelines/object_detection
CMD ["/home/detect-object.py"]

####
ARG  UID
USER ${UID}
####
