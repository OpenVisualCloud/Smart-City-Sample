
FROM openvisualcloud/xeon-centos76-media-ffmpeg:latest

RUN yum -y install epel-release && yum -y install python36-requests python36-ply python36-pip gcc python3-devel && rm -rf /var/cache/yum/* curl
RUN pip3 install psutil

COPY --from=smtc_common /*.py /home/
COPY    *.py /home/
CMD     ["/home/smart-upload.py"]

####
ARG  USER
ARG  GROUP
ARG  UID
ARG  GID
## must use ; here to ignore user exist status code
RUN  [ ${GID} -gt 0 ] && groupadd -f -g ${GID} ${GROUP}; \
     [ ${UID} -gt 0 ] && useradd -d /home/${USER} -g ${GID} -K UID_MAX=${UID} -K UID_MIN=${UID} ${USER}; \
     echo
USER ${UID}
####
