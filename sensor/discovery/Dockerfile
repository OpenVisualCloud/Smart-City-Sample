
FROM openvisualcloud/xeon-centos76-media-ffmpeg:20.4

RUN yum install -y -q epel-release nmap && yum -y -q install python36-ply python36-requests python36-setuptools && rm -rf /var/cache/yum/*

ARG ZEEP_VER=3.4.0
ARG ZEEP_REPO=https://github.com/mvantellingen/python-zeep/archive/${ZEEP_VER}.tar.gz
ARG ONVIF_ZEEP_VER=0.2.12
ARG ONVIF_ZEEP_REPO=https://github.com/FalkTannhaeuser/python-onvif-zeep/archive/v${ONVIF_ZEEP_VER}.tar.gz

RUN  curl -L ${ZEEP_REPO} | tar xz && \
     cd python-zeep-${ZEEP_VER} && \
     python3 setup.py build && \
     python3 setup.py install && \
     cd .. && \
     rm -rf python-zeep-${ZEEP_VER} && \
     curl -L ${ONVIF_ZEEP_REPO} | tar xz && \
     cd python-onvif-zeep-${ONVIF_ZEEP_VER} && \
     cp -r wsdl /home && \
     python3 setup.py build && \
     python3 setup.py install && \
     cd .. && \
     rm -rf python-onvif-zeep-${ONVIF_ZEEP_VER}

COPY --from=smtc_common /home/*.py /home/
COPY *.py /home/
CMD  ["/home/discover.py"]
ENV  PYTHONIOENCODING=UTF-8

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
