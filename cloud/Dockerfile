
FROM centos:7.6.1810

RUN yum -y install epel-release && yum -y install nginx python36-tornado python36-requests python36-ply python36-psutil && rm -rf /var/cache/yum/*

COPY    *.conf /etc/nginx/
COPY    *.py /home/
COPY    html /var/www/html
CMD     ["/home/webc.py"]
EXPOSE  8080

####
ARG  USER
ARG  GROUP
ARG  UID
ARG  GID
## must use ; here to ignore user exist status code
RUN  [ ${GID} -gt 0 ] && groupadd -f -g ${GID} ${GROUP}; \
     [ ${UID} -gt 0 ] && useradd -d /home/${USER} -g ${GID} -K UID_MAX=${UID} -K UID_MIN=${UID} ${USER}; \
     touch /var/run/nginx.pid && \
     mkdir -p /var/log/nginx /var/lib/nginx /var/www/cache /var/www/thumbnail && \
     chown -R ${UID}.${GID} /var/run/nginx.pid /var/www /var/log/nginx /var/lib/nginx /etc/nginx/resolver.conf
USER ${UID}
####
