
FROM openvisualcloud/xeon-ubuntu2004-media-nginx:21.6.1

RUN DEBIAN_FRONTEND=noninteractive apt-get update -qq && apt-get install -qq python3-tornado python3-requests python3-ply && rm -rf /var/lib/apt/lists/*

COPY --from=smtc_common /home/*.py /home/
COPY --from=smtc_sensor_webrtc /home/owt/apps/current_app/public/scripts/owt.js /var/www/html/js/vendor/
COPY *.conf /etc/nginx/
COPY *.py /home/
COPY html /var/www/html
CMD  ["/home/webc.py"]
ENV  PYTHONIOENCODING=UTF-8

####
ARG  USER=docker
ARG  GROUP=docker
ARG  UID
ARG  GID
## must use ; here to ignore user exist status code
RUN  [ ${GID} -gt 0 ] && groupadd -f -g ${GID} ${GROUP}; \
     [ ${UID} -gt 0 ] && useradd -d /home -M -g ${GID} -K UID_MAX=${UID} -K UID_MIN=${UID} ${USER}; \
     touch /var/www/nginx.pid && \
     mkdir -p /var/log/nginx /var/lib/nginx /var/www/cache /var/www/thumbnail && \
     chown -R ${UID}:${GID} /var/www/nginx.pid /var/www/log /var/log/nginx /var/lib/nginx /etc/nginx/upstream.conf /var/www/html/js/scenario.js
USER ${UID}
####
