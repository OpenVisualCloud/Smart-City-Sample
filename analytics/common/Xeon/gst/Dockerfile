# smtc_analytics_common_xeon_gst

FROM openvisualcloud/xeon-ubuntu1804-analytics-gst:20.4 as build

RUN DEBIAN_FRONTEND=noninteractive apt-get update -qq && apt-get install -qq git ca-certificates
ARG VA_SERVING_REPO=https://github.com/intel/video-analytics-serving.git
ARG VA_SERVING_BRANCH="v0.3_preview"
ARG VA_SERVING_TAG="1b342051b85682beadb1ec173f848697fa2f02b2"

RUN git clone ${VA_SERVING_REPO} -b ${VA_SERVING_BRANCH} --depth 1
RUN cd video-analytics-serving; git checkout ${VA_SERVING_TAG}
RUN rm -rf /home/video-analytics-serving/vaserving/__main__.py
RUN rm -rf /home/video-analytics-serving/vaserving/rest_api

FROM openvisualcloud/xeon-ubuntu1804-analytics-gst:20.4

RUN DEBIAN_FRONTEND=noninteractive apt-get update -qq && apt-get install -qq python3-gst-1.0 python3-jsonschema python3-psutil && rm -rf /var/lib/apt/lists/*

COPY --from=build /home/video-analytics-serving/vaserving /home/vaserving
ENV  FRAMEWORK=gstreamer
COPY *.py /home/
