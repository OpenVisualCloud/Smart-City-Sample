
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
## VLC must run as nonroot
## must use ; here to ignore user exist status code
RUN  groupadd ${GROUP}; \
     useradd -d /home/${USER} -g ${GROUP} ${USER}; \
     chown -R ${USER}.${GROUP} /home
USER ${USER}
####
