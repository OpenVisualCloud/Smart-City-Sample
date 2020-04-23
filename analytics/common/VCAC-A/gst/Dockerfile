# smtc_analytics_common_vcac-a_gst

FROM smtc_analytics_common_vcac-a_gst_base

# Fetch python3 and Install python3
RUN DEBIAN_FRONTEND=noninteractive apt-get update && apt-get install -y -q --no-install-recommends libjson-c3 python3-gst-1.0 python3-jsonschema &&  rm -rf /var/lib/apt/lists/*;
COPY VCAC-A/gst/frame.py /usr/lib/python3.6/gstgva/
COPY app /home/
COPY *.py /home/
