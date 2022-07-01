# smtc_analytics_common_xeon_gst

FROM ubuntu:20.04 as build

RUN DEBIAN_FRONTEND=noninteractive apt-get update -qq && apt-get install -qq curl && rm -rf /var/lib/apt/lists/*

ARG  VA_SERVING_REPO=https://raw.githubusercontent.com/intel/video-analytics-serving
ARG  VA_SERVING_TAG="v0.4.1-beta"

RUN  mkdir -p /home/vaserving/common/utils && touch /home/vaserving/__init__.py /home/vaserving/common/__init__.py /home/vaserving/common/utils/__init__.py && for x in common/utils/logging.py common/settings.py arguments.py ffmpeg_pipeline.py gstreamer_pipeline.py app_destination.py app_source.py gstreamer_app_destination.py gstreamer_app_source.py model_manager.py pipeline.py pipeline_manager.py pipeline.py schema.py vaserving.py; do curl -sSf -o /home/vaserving/$x -L ${VA_SERVING_REPO}/${VA_SERVING_TAG}/vaserving/$x; done
COPY *.py /home/

FROM openvisualcloud/xeon-ubuntu2004-analytics-gst:21.6.1

RUN  apt-get update -qq && apt-get install -qq python3-gst-1.0 python3-jsonschema python3-psutil && rm -rf /var/lib/apt/lists/*

COPY --from=build /home/ /home/
ENV  FRAMEWORK=gstreamer
ENV  PYTHONIOENCODING=UTF-8

####
ARG  USER=docker
ARG  GROUP=docker
ARG  UID
ARG  GID
## must use ; here to ignore user exist status code
RUN  [ ${GID} -gt 0 ] && groupadd -f -g ${GID} ${GROUP}; \
     [ ${UID} -gt 0 ] && useradd -d /home -M -g ${GID} -K UID_MAX=${UID} -K UID_MIN=${UID} ${USER}; \
     chown -R ${UID}:${GID} /home
####

