
FROM openvisualcloud/xeon-centos7-media-ffmpeg:21.6

RUN yum install -y -q epel-release && yum -y -q install python36-ply python36-requests python36-setuptools && rm -rf /var/cache/yum/*

COPY --from=smtc_common /home/*.py /home/
COPY *.py /home/
CMD  ["/home/discover.py"]
ENV  PYTHONIOENCODING=UTF-8

####
ARG  USER=docker
ARG  GROUP=docker
ARG  UID
ARG  GID
## must use ; here to ignore user exist status code
RUN  [ ${GID} -gt 0 ] && groupadd -f -g ${GID} ${GROUP}; \
     [ ${UID} -gt 0 ] && useradd -d /home -M -g ${GID} -K UID_MAX=${UID} -K UID_MIN=${UID} ${USER}; \
     chown -R ${UID}:${GID} /home
USER ${UID}
####
