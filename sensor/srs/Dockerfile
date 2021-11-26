
FROM openvisualcloud/xeon-ubuntu1804-media-srs:21.6.1

RUN mkdir -p /usr/local/srs/objs/ffmpeg/bin/ && cp /usr/local/bin/ffmpeg /usr/local/srs/objs/ffmpeg/bin/ffmpeg

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

