
ARG tag=v4.0.56
ARG url=https://gitee.com/winlinvip/srs.oschina.git

############################################################
# build
############################################################
ARG repo=registry.cn-hangzhou.aliyuncs.com/ossrs/srs:dev
FROM ${repo} AS build
ARG tag
ARG url
# Install required tools.
RUN yum install -y gcc make gcc-c++ patch unzip perl git
RUN cd /tmp && git clone --depth=1 --branch ${tag} ${url} srs
RUN cd /tmp/srs/trunk && ./configure --with-gb28181 --with-research && make && make install
ARG docker_url=https://github.com/ossrs/srs-docker.git
RUN cd /tmp && git clone --depth=1 --branch ${tag} ${docker_url} srs-docker 
RUN cp /tmp/srs-docker/index.html /usr/local/srs/objs/nginx/html/index.html
RUN cp -r /tmp/srs-docker/srs-console/trunk/research/console /usr/local/srs/objs/nginx/html/console

############################################################
# dist
############################################################
FROM centos:7 AS dist
# FFMPEG 4.1
COPY --from=build /usr/local/bin/ffmpeg /usr/local/srs/objs/ffmpeg/bin/ffmpeg
# SRS binary, config files and srs-console.
COPY --from=build /usr/local/srs /usr/local/srs
# Default workdir and command.
COPY --from=smtc_common /home/*.py /home/
COPY *.py /home/

WORKDIR /usr/local/srs
CMD ["./objs/srs", "-c", "conf/srs.conf"]

####
ARG  UID
ARG  GID
# must use ; here to ignore user exist status code
RUN  [ ${GID} -gt 0 ] && groupadd -f -g ${GID} docker; \
     [ ${UID} -gt 0 ] && useradd -d /home/docker -g ${GID} -K UID_MAX=${UID} -K UID_MIN=${UID} docker; \
     chown -R ${UID}:${GID} /usr/local/srs 
USER ${UID}
####

