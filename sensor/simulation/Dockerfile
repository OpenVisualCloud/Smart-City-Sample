
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
RUN  groupadd -f -g ${GID} ${GROUP};useradd -d /home/${USER} -g ${GROUP} -K UID_MAX=${UID} -K UID_MIN=${UID} ${USER};chown -R ${USER}.${GROUP} /home
USER ${USER}
####
