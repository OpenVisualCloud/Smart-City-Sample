
FROM centos:7.6.1810

RUN yum install -y epel-release && yum install -y python36-requests python36-ply && rm -rf /var/cache/yum/*
COPY --from=smtc_common /*.py /home/
COPY *.py /home/
CMD  ["/home/check.py"]

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

