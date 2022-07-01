
FROM ubuntu:20.04

RUN DEBIAN_FRONTEND=noninteractive apt-get update -qq && apt-get install -qq openssh-client && rm -rf /var/lib/apt/lists/*
COPY *.sh /home/
CMD  ["/home/tunnel.sh"]
WORKDIR /home

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

