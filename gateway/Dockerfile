
FROM openvisualcloud/xeon-centos7-media-nginx:21.6

RUN yum install -y -q epel-release && yum install -y -q python36-tornado python36-requests python36-ply python36-psutil && rm -rf /var/cache/yum/*

COPY --from=smtc_common /home/*.py /home/
COPY    *.py /home/
COPY    *.conf /etc/nginx/
CMD     ["/home/gateway.py"]
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
     chown -R ${UID}:${GID} /home /var/run/nginx.pid /var/log/nginx /var/lib/nginx /var/www /etc/nginx/upstream.conf
USER ${UID}
####
