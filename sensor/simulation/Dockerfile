
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
## VLC must run as a non-root user.
## must use ; here to ignore user exist status code
RUN  groupadd -f -g 9999 ${GROUP}; \
     useradd -d /home/${USER} -g 9999 -K UID_MAX=9999 -K UID_MIN=9999 ${USER}; \
     echo
USER 9999
####
