
FROM centos:7.6.1810

RUN yum install -y -q epel-release && yum install -y -q python36-requests python36-ply python36-psutil && rm -rf /var/cache/yum/*

COPY *.py /home/
ENV  PYTHONIOENCODING=UTF-8
