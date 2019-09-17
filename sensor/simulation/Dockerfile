
FROM ubuntu:18.04
RUN apt-get update && apt-get install -y -q python3-requests vlc && rm -rf /var/lib/apt/lists/*
COPY *.py /home/
COPY *.mp4 /mnt/simulated/
CMD ["/home/simulate.py"]

####
ARG  USER
ARG  GROUP
ARG  UID
ARG  GID
## must use ; here to ignore user exist status code
RUN  [[ ${GID} -gt 0 ]] && groupadd -f -g ${GID} ${GROUP}; \
     [[ ${UID} -gt 0 ]] && useradd -d /home/${USER} -g ${GID} -K UID_MAX=${UID} -K UID_MIN=${UID} ${USER}; \
     echo
USER ${UID}
####
