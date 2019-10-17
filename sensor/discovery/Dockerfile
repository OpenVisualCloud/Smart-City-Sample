FROM ubuntu:18.04

RUN  DEBIAN_FRONTEND=noninteractive apt-get update && apt-get install -y -q python3-ply nmap wget python3-setuptools ffmpeg vim && rm -rf /var/lib/apt/lists/*

ARG ZEEP_VER=3.3.1
ARG ZEEP_REPO=https://github.com/mvantellingen/python-zeep/archive/${ZEEP_VER}.tar.gz
ARG ONVIF_ZEEP_VER=0.2.12
ARG ONVIF_ZEEP_REPO=https://github.com/FalkTannhaeuser/python-onvif-zeep/archive/v${ONVIF_ZEEP_VER}.tar.gz

RUN  wget ${ZEEP_REPO} && \
     tar -xf ${ZEEP_VER}.tar.gz && \
     cd python-zeep-${ZEEP_VER} && \
     python3 setup.py build && \
     python3 setup.py install && \
     cd .. && \
     rm -rf python-zeep-${ZEEP_VER} && \
     rm ${ZEEP_VER}.tar.gz && \
     wget ${ONVIF_ZEEP_REPO} && \
     tar -xf v${ONVIF_ZEEP_VER}.tar.gz && \
     cd python-onvif-zeep-${ONVIF_ZEEP_VER} && \
     cp -r wsdl /home && \
     python3 setup.py build && \
     python3 setup.py install && \
     cd .. && \
     rm -rf python-onvif-zeep-${ONVIF_ZEEP_VER} && \
     rm v${ONVIF_ZEEP_VER}.tar.gz

COPY --from=smtc_common /*.py /home/
COPY    *.py /home/
CMD     ["/home/discover.py"]
WORKDIR /home

####
ARG  USER
ARG  GROUP
ARG  UID
ARG  GID
## must use ; here to ignore user exist status code
RUN  [ ${GID} -gt 0 ] && groupadd -f -g ${GID} ${GROUP}; \
     [ ${UID} -gt 0 ] && useradd -d /home/${USER} -g ${GID} -K UID_MAX=${UID} -K UID_MIN=${UID} ${USER}; \
     chown -R ${UID}.${GID} /home
USER ${UID}
####
