
FROM openvisualcloud/xeon-centos76-media-ffmpeg:20.4
RUN  yum install -y -q epel-release && yum install -y -q python36-requests python36-ply python36-psutil && rm -rf /var/cache/yum/* curl

COPY --from=smtc_common /home/*.py /home/
COPY *.py /home/
CMD  ["/home/smart-upload.py"]
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
