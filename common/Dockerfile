
FROM ubuntu:20.04

RUN DEBIAN_FRONTEND=noninteractive apt-get update -qq && \
    apt-get install -qq python3-requests python3-ply python3-psutil python3-pip && \
    rm -rf /var/lib/apt/lists/*

COPY *.py /home/
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
####

