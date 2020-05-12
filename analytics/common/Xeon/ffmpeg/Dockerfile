# smtc_analytics_common_xeon_ffmpeg

From openvisualcloud/xeon-ubuntu1804-analytics-ffmpeg:20.1
RUN DEBIAN_FRONTEND=noninteractive apt-get update -qq && apt-get install -qq python3-gst-1.0 python3-jsonschema python3-psutil && rm -rf /var/lib/apt/lists/*

COPY app /home/
COPY *.py /home/
