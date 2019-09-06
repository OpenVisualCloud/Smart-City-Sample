
FROM centos:7.6.1810

RUN yum install -y epel-release && yum install -y python36-requests python36-ply curl && rm -rf /var/cache/yum/*
COPY *.py /home/
CMD  ["/home/check.py"]

####
ARG  USER
ARG  GROUP
ARG  UID
ARG  GID
## must use ; here to ignore user exist status code
RUN  groupadd -f -g ${GID} ${GROUP};useradd -d /home/${USER} -g ${GROUP} -K UID_MAX=${UID} -K UID_MIN=${UID} ${USER};echo
USER ${USER}
####

