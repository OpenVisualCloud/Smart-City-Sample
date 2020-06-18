# smtc_analytics_object_vcac-a_gst

FROM smtc_analytics_common_vcac-a_gst

RUN  apt-get update -qq && apt-get install -qq python3-paho-mqtt python3-ply python3-requests python3-watchdog && rm -rf /var/lib/apt/lists/*

COPY --from=smtc_common /home/*.py /home/
COPY *.py /home/
COPY models /home/models
COPY VCAC-A/gst/pipeline /home/pipelines/object_detection
CMD ["/home/detect-object.py"]

####
ARG  UID
USER ${UID}
####
