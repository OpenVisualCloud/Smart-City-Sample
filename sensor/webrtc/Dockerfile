
FROM openvisualcloud/xeon-ubuntu1804-service-owt:21.6.1

RUN  apt-get update -q && apt-get install -y -q nginx python3-tornado python3-requests python3-ply && rm -rf /var/lib/apt/lists/*

COPY *.conf /etc/nginx/
RUN  sed -i "s/io(e,a)/io(undefined,Object.assign(a,{path:window.sessionStorage.officePath+'\/socket.io\/'}))/" /home/owt/apps/current_app/public/scripts/owt.js && \
     sed -i "s/^ssl =.*/ssl = false/" /home/owt/portal/portal.toml && \
     sed -i "s/^ssl =.*/ssl = false/" /home/owt/management_api/management_api.toml
COPY --from=smtc_common /home/*.py /home/
COPY launch.sh config.sh /home/
COPY *.py /home/

CMD  ["/home/launch.sh","/home/webs.py"]
ENV  PYTHONIOENCODING=UTF-8

####
ARG  USER=docker
ARG  GROUP=docker
ARG  UID
ARG  GID
## must use ; here to ignore user exist status code
RUN  [ ${GID} -gt 0 ] && groupadd -f -g ${GID} ${GROUP}; \
     [ ${UID} -gt 0 ] && useradd -d /home -M -g ${GID} -K UID_MAX=${UID} -K UID_MIN=${UID} ${USER}; \
     touch /var/run/nginx.pid && \
     mkdir -p /var/log/nginx /var/lib/nginx && \
     chown ${UID}:${GID} $(find /home -maxdepth 2 -type d -print) /var/run/nginx.pid /home/owt/*/*.toml /home/owt/apps/current_app/main.js && \
     chown -R ${UID}:${GID} /var/log/nginx /var/lib/nginx
USER ${UID}
####
