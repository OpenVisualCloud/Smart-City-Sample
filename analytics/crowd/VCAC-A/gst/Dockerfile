# smtc_analytics_crowd_vcac-a_gst

FROM smtc_analytics_common_vcac-a_gst

RUN  apt-get update -qq && apt-get install -qq python3-paho-mqtt python3-ply python3-requests python3-watchdog python3-pillow && rm -rf /var/lib/apt/lists/*

COPY --from=smtc_common /home/*.py /home/
COPY *.py /home/
COPY models/CSRNet_IR_model_2020R2/2 /home/models/CSRNet_IR_model_2020R2/2
COPY VCAC-A/gst/pipeline /home/pipelines/crowd_counting
COPY custom_transforms /home/custom_transforms
CMD  ["/home/count-crowd.py"]
ENV  PATH=${PATH}:/home/custom_transforms

####
ARG  UID
USER ${UID}
####
