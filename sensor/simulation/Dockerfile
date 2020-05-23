
FROM ubuntu:18.04
RUN apt-get update -qq && apt-get install -qq python3-requests vlc && rm -rf /var/lib/apt/lists/*
COPY *.py /home/
COPY archive/*.mp4 /mnt/simulated/
CMD ["/home/simulate.py"]

####
ARG  USER=docker
ARG  GROUP=docker
ARG  UID
ARG  GID
## VLC must run as nonroot
## must use ; here to ignore user exist status code
RUN  groupadd ${GROUP}; \
     useradd -d /home/${USER} -g ${GROUP} ${USER}; \
     chown -R ${USER}:${GROUP} /home
USER ${USER}
####
