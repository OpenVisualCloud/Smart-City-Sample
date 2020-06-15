
    cloud_web:
        image: defn(`REGISTRY_PREFIX')smtc_web_cloud:latest
        ports:
            - target: 8443
              published: 443
              protocol: tcp
              mode: host
        environment:
            DBHOST: "http://ifelse(eval(defn(`NOFFICES')>1),1,cloud_db,db):9200"
            PROXYHOST: "http://cloud_storage:8080"
            `SCENARIO': "defn(`SCENARIO')"
            HEALTH_CHECK: "ifelse(eval(defn(`NOFFICES')>1),1,enabled,disabled)"
            NO_PROXY: "*"
            no_proxy: "*"
        volumes:
            - /etc/localtime:/etc/localtime:ro
        secrets:
            - source: self_crt
              target: self.crt
              uid: ${USER_ID}
              gid: ${GROUP_ID}
              mode: 0444
            - source: self_key
              target: self.key
              uid: ${USER_ID}
              gid: ${GROUP_ID}
              mode: 0440
        networks:
            - appnet
        deploy:
            placement:
                constraints:
                    - node.role==manager
                    - node.labels.vcac_zone!=yes
