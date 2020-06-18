
FROM smtc_common
RUN  pip3 install paho-mqtt==1.3.0
COPY *.py /home/
CMD  ["/home/mqtt2db.py"]

####
ARG  UID
USER ${UID}
####
