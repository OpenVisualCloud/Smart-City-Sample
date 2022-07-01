
FROM openvisualcloud/xeon-ubuntu2004-media-nginx:21.6.1

RUN DEBIAN_FRONTEND=noninteractive apt-get update -qq && apt-get install -qq python3-tornado python3-requests python3-ply python3-psutil && rm -rf /var/lib/apt/lists/*

COPY --from=smtc_common /home/*.py /home/
COPY    *.py /home/
COPY    *.conf /etc/nginx/
CMD     ["/home/storage.py"]
ENV     PYTHONIOENCODING=UTF-8

####
ARG  USER=docker
ARG  GROUP=docker
ARG  UID
ARG  GID
## must use ; here to ignore user exist status code
RUN  [ ${GID} -gt 0 ] && groupadd -f -g ${GID} ${GROUP}; \
     [ ${UID} -gt 0 ] && useradd -d /home -M -g ${GID} -K UID_MAX=${UID} -K UID_MIN=${UID} ${USER}; \
     touch /var/run/nginx.pid && \
     mkdir -p /var/log/nginx /var/lib/nginx /var/www/cache /var/www/upload /var/www/mp4 && \
     chown -R ${UID}:${GID} /home /var/run/nginx.pid /var/log/nginx /var/lib/nginx /var/www /etc/nginx/nginx.conf
USER ${UID}
####
