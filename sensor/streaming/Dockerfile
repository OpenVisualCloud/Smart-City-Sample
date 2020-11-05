
FROM openvisualcloud/xeon-ubuntu1804-media-nginx:20.7

Run DEBIAN_FRONTEND=noninteractive apt-get update && apt-get install -y -q --no-install-recommends python3-tornado python3-requests python3-ply python3-psutil && rm -rf /var/lib/apt/lists/*

COPY *.conf /etc/nginx/

CMD  ["/usr/local/sbin/nginx"]
ENV  PYTHONIOENCODING=UTF-8

####
ARG  UID
ARG  GID
## must use ; here to ignore user exist status code
RUN  [ ${GID} -gt 0 ] && groupadd -f -g ${GID} docker; \
     [ ${UID} -gt 0 ] && useradd -d /home/docker -g ${GID} -K UID_MAX=${UID} -K UID_MIN=${UID} docker; \
     touch /var/run/nginx.pid && \
     mkdir -p /var/log/nginx /var/lib/nginx /var/www/video /var/www/archive && \
     chown -R ${UID}:${GID} /var/run/nginx.pid /var/www /var/log/nginx /var/lib/nginx
USER ${UID}
####
