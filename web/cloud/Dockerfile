
FROM openvisualcloud/xeon-centos76-media-ffmpeg

RUN yum -y install epel-release && yum -y install nginx python36-tornado python36-requests python36-ply python36-psutil && rm -rf /var/cache/yum/*

COPY    *.conf /etc/nginx/
COPY    *.py /home/
COPY    html /var/www/html
CMD     ["/home/main.py"]
EXPOSE  8080

####
ARG  USER
ARG  GROUP
ARG  UID
ARG  GID
## must use ; here to ignore user exist status code
RUN  groupadd -f -g ${GID} ${GROUP};useradd -d /home/${USER} -g ${GROUP} -K UID_MAX=${UID} -K UID_MIN=${UID} ${USER}; \
     touch /var/run/nginx.pid && \
     mkdir -p /var/log/nginx /var/lib/nginx /var/www/cache /var/www/thumbnail && \
     chown -R ${USER}.${GROUP} /var/run/nginx.pid /var/www /var/log/nginx /var/lib/nginx
USER ${USER}
####
