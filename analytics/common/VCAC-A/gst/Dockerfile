# smtc_analytics_common_vcac-a_gst

FROM centos:7.6.1810 as build

ARG VA_SERVING_REPO=https://github.com/intel/video-analytics-serving
ARG VA_SERVING_TAG="v0.3.0-alpha"

RUN curl -L ${VA_SERVING_REPO}/archive/${VA_SERVING_TAG}.tar.gz | tar -xz && \
    mv video-analytics-serving* video-analytics-serving && \
    rm -rf video-analytics-serving/vaserving/__main__.py && \
    rm -rf video-analytics-serving/vaserving/rest_api

FROM openvisualcloud/vcaca-ubuntu1804-analytics-gst:20.4

RUN DEBIAN_FRONTEND=noninteractive apt-get update -qq && apt-get install -qq python3-gst-1.0 python3-jsonschema python3-psutil && rm -rf /var/lib/apt/lists/*

COPY --from=build /video-analytics-serving/vaserving /home/vaserving
ENV  FRAMEWORK=gstreamer
COPY *.py /home/
