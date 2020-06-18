
FROM ubuntu:18.04
RUN apt-get update -qq && apt-get install -qq python3-requests vlc && rm -rf /var/lib/apt/lists/*
COPY *.py /home/
COPY archive/*.mp4 /mnt/simulated/
CMD ["/home/simulate.py"]
ENV  PYTHONIOENCODING=UTF-8

####
ARG  USER=docker
ARG  GROUP=docker
## VLC must run as nonroot
RUN  groupadd ${GROUP} && \
     useradd -d /home/${USER} -g ${GROUP} ${USER}
USER ${USER}
####
