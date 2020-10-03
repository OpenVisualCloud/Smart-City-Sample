
FROM openvisualcloud/xeon-centos76-media-nginx:20.7

RUN  yum install -y -q epel-release && yum install -y -q python36-tornado python36-requests python36-ply && rm -rf /var/cache/yum/*

COPY --from=smtc_common /home/*.py /home/
COPY --from=smtc_sensor_webrtc /home/owt/extras/basic_example/public/scripts/owt.js /var/www/html/js/vendor/
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
