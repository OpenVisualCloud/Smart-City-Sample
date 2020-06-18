
FROM smtc_common
COPY *.py /home/
CMD  ["/bin/sh","-c","/home/db-init.py && /home/provision.py"]

####
ARG  UID
USER ${UID}
####
