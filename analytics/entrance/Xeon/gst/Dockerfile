# smtc_analytics_entrance_xeon_gst

FROM smtc_analytics_common_xeon_gst
RUN  apt-get update -qq && apt-get install -qq python3-paho-mqtt python3-ply python3-requests python3-watchdog python3-munkres && rm -rf /var/lib/apt/lists/*

COPY --from=smtc_common /home/*.py /home/
COPY *.py /home/
COPY models /home/models
COPY Xeon/gst/pipeline /home/pipelines/entrance_counting
COPY custom_transforms /home/custom_transforms
CMD ["/home/count-entrance.py"]
ENV PATH=${PATH}:/home/custom_transforms

####
ARG  UID
USER ${UID}
####
