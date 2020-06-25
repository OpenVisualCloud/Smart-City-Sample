
FROM smtc_common
RUN  yum install -y -q openssh-clients && rm -rf /var/cache/yum/*
COPY *.sh /home/
CMD  ["/home/tunnel-create.sh"]
WORKDIR /home

####
ARG  UID
USER ${UID}
####

