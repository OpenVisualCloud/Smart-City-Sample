
FROM smtc_common
RUN  pip3 install paho-mqtt==1.3.0
COPY *.py /home/
CMD  ["/home/mqtt2db.py"]

####
ARG  USER
ARG  GROUP
ARG  UID
ARG  GID
## must use ; here to ignore user exist status code
RUN  [ ${GID} -gt 0 ] && groupadd -f -g ${GID} ${GROUP}; \
     [ ${UID} -gt 0 ] && useradd -d /home/${USER} -g ${GID} -K UID_MAX=${UID} -K UID_MIN=${UID} ${USER}; \
     echo
USER ${UID}
####
