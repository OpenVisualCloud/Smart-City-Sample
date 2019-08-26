
FROM centos:7.6.1810

RUN yum -y install epel-release && yum -y install python36-requests python36-ply && rm -rf /var/cache/yum/*

COPY    *.py /home/
CMD     ["/home/index.py"]

####
ARG  USER
ARG  GROUP
ARG  UID
ARG  GID
## must use ; here to ignore user exist status code
RUN  groupadd -f -g ${GID} ${GROUP};useradd -d /home/${USER} -g ${GROUP} -K UID_MAX=${UID} -K UID_MIN=${UID} ${USER};echo
USER ${USER}
####
