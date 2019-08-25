    cloud_db:
        image: docker.elastic.co/elasticsearch/elasticsearch-oss:6.8.1
        environment:
ifelse(eval(defn(`NOFFICES')>1),1,`dnl
            - "cluster.name=db-cluster"
            - "node.name=cloud_db"
            - "node.master=true"
            - "node.data=false"
',`dnl
            - "discovery.type=single-node"
')dnl
            - "action.auto_create_index=0"
            - "ES_JAVA_OPTS=-Xms4096m -Xmx4096m"
            - "NO_PROXY=*"
            - "no_proxy=*"
        networks:
            - db_net
        deploy:
            placement:
                constraints: [node.role==manager]

    cloud_web:
        image: smtc_web_cloud:latest
        ports:
            - "443:8080"
        environment:
            DBHOST: "http://cloud_db:9200"
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
            - source: dhparam_pem
              target: dhparam.pem
              uid: ${USER_ID}
              gid: ${GROUP_ID}
              mode: 0444
        networks:
            - db_net
forloop(`id',1,defn(`NOFFICES'),`dnl
ifdef(`location_office'defn(`id'),`dnl
            - `office'defn(`id')_net
')dnl
')dnl
        deploy:
            placement:
                constraints: [node.role==manager]
