# smtc_analytics_common_xeon_gst
#FROM openvisualcloud/xeon-ubuntu1804-analytics-gst:20.1 as build
FROM smtc_analytics_common_xeon_gst_base as vaserving_build
RUN DEBIAN_FRONTEND=noninteractive apt-get update -qq && apt-get install -qq git ca-certificates python3 python3-pip && rm -rf /var/lib/apt/lists/*
ARG VA_SERVING_REPO=https://gitlab.devtools.intel.com/video-analytics/video-analytics-serving.git
ARG VA_SERVING_BRANCH="ovc_integration"
ARG VA_SERVING_TAG="05b38b6449199ef7b98806eab9292f5a0123c2cd"

RUN  git clone ${VA_SERVING_REPO} -b ${VA_SERVING_BRANCH} --depth 1
RUN  cd video-analytics-serving; git checkout ${VA_SERVING_TAG}
RUN pip3 install --ignore-installed --target /home/build -r video-analytics-serving/requirements.txt
RUN rm -rf /home/video-analytics-serving/vaserving/__main__.py
RUN rm -rf /home/video-analytics-serving/vaserving/rest_api

FROM smtc_analytics_common_xeon_gst_base

RUN DEBIAN_FRONTEND=noninteractive apt-get update -qq && apt-get install -qq python3-gst-1.0 python3-jsonschema && rm -rf /var/lib/apt/lists/*

COPY --from=vaserving_build /home/build/ /usr/lib/python3/dist-packages
COPY --from=vaserving_build /home/video-analytics-serving/vaserving /home/vaserving
COPY *.py /home/
