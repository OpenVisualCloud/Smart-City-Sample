
FROM centos:7.6.1810 

RUN yum install -y -q epel-release && yum install -y -q openssh-clients && rm -rf /var/cache/yum/*
COPY custom-entrypoint.sh /usr/local/bin/
RUN  chmod 777 /usr/local/bin/custom-entrypoint.sh
CMD ["/usr/local/bin/custom-entrypoint.sh"]

