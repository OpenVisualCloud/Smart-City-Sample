
ifelse(eval(defn(`NOFFICES')>1),1,`

    defn(`OFFICE_NAME')_db:
        image: docker.elastic.co/elasticsearch/elasticsearch-oss:6.8.1
        environment:
            - "cluster.name=db-cluster"
            - "node.name=defn(`OFFICE_NAME')"
            - "node.master=false"
            - "node.data=true"
            - "node.attr.zone=defn(`OFFICE_NAME')"
            - "discovery.zen.minimum_master_nodes=1"
            - "discovery.zen.ping.unicast.hosts=cloud_db"
            - "action.auto_create_index=0"
            - "ES_JAVA_OPTS=-Xms4096m -Xmx4096m"
            - "NO_PROXY=*"
            - "no_proxy=*"
        volumes:
            - /etc/localtime:/etc/localtime:ro
        networks:
            - appnet
        deploy:
            placement:
                constraints:
                    - node.labels.vcac_zone!=yes
')

    defn(`OFFICE_NAME')_db_init:
        image: defn(`REGISTRY_PREFIX')smtc_db_init:latest
        environment:
            DBHOST: "http://ifelse(eval(defn(`NOFFICES')>1),1,cloud_db,db):9200"
            OFFICE: "defn(`OFFICE_LOCATION')"
            PROXYHOST: "http://defn(`OFFICE_NAME')_storage:8080"
            `SCENARIO': "defn(`SCENARIO_NAME')"
            ZONE: "defn(`OFFICE_NAME')"
            NO_PROXY: "*"
            no_proxy: "*"
        secrets:
            - source: sensor_info
              target: sensor-info.json
              uid: "${USER_ID}"
              gid: "${GROUP_ID}"
              mode: 0444
        volumes:
            - /etc/localtime:/etc/localtime:ro
        networks:
            - appnet
        deploy:
            restart_policy:
                condition: none
            placement:
                constraints:
                    - node.labels.vcac_zone!=yes
