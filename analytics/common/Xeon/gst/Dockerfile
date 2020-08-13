# smtc_analytics_common_xeon_gst

FROM centos:7.6.1810 as build

ARG  VA_SERVING_REPO=https://raw.githubusercontent.com/intel/video-analytics-serving
ARG  VA_SERVING_TAG="v0.3.0-alpha"

RUN  mkdir -p /home/vaserving/common/utils && touch /home/vaserving/__init__.py /home/vaserving/common/__init__.py /home/vaserving/common/utils/__init__.py && for x in common/utils/logging.py common/settings.py arguments.py ffmpeg_pipeline.py gstreamer_pipeline.py model_manager.py pipeline.py pipeline_manager.py schema.py vaserving.py; do curl -o /home/vaserving/$x -L ${VA_SERVING_REPO}/${VA_SERVING_TAG}/vaserving/$x; done
COPY *.py /home/

FROM openvisualcloud/xeon-ubuntu1804-analytics-gst:20.4

RUN DEBIAN_FRONTEND=noninteractive apt-get update -qq && apt-get install -qq python3-gst-1.0 python3-jsonschema python3-psutil && rm -rf /var/lib/apt/lists/*

COPY --from=build /home/video-analytics-serving/vaserving /home/vaserving
ENV  FRAMEWORK=gstreamer
COPY *.py /home/
