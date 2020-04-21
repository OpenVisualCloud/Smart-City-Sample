# smtc_analytics_common_xeon_gst
FROM openvisualcloud/xeon-ubuntu1804-analytics-gst:20.1 as build
RUN DEBIAN_FRONTEND=noninteractive apt-get update -qq && apt-get install -qq git ca-certificates python3 python3-pip && rm -rf /var/lib/apt/lists/*
ARG VA_SERVING_REPO=https://gitlab.devtools.intel.com/video-analytics/video-analytics-serving.git
ARG VA_SERVING_TAG=develop

RUN  git clone ${VA_SERVING_REPO} -b ${VA_SERVING_TAG} --depth 1

RUN pip3 install --ignore-installed --target /home/build -r video-analytics-serving/service/app/server/requirements.txt
RUN pwd

FROM openvisualcloud/xeon-ubuntu1804-analytics-gst:20.1

RUN DEBIAN_FRONTEND=noninteractive apt-get update -qq && apt-get install -qq python3-gst-1.0 python3-jsonschema && rm -rf /var/lib/apt/lists/*

COPY --from=build /home/build/ /usr/lib/python3/dist-packages
COPY --from=build /home/video-analytics-serving/service/app/modules /home/video-analytics-serving/modules
COPY *.py /home/
