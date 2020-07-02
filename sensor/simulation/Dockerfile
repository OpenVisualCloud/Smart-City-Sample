
FROM ubuntu:18.04
RUN  apt-get update -qq && apt-get install -qq python3-requests python3-ply vlc && rm -rf /var/lib/apt/lists/*
COPY *.py /home/
COPY archive/*.mp4 /mnt/simulated/
COPY --from=smtc_common /home/*.py /home/
CMD  ["/home/simulate.py"]
ENV  PYTHONIOENCODING=UTF-8

####
ARG  USER=docker
ARG  GROUP=docker
## VLC must run as nonroot
RUN  groupadd ${GROUP} && \
     useradd -d /home -M -g ${GROUP} ${USER} && \
     chown -R ${USER}:${GROUP} /home
USER ${USER}
####
