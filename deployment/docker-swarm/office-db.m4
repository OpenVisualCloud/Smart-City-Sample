
ifelse(defn(`NOFFICES'),1,,`

    defn(`OFFICE_NAME')_db:
        image: docker.elastic.co/elasticsearch/elasticsearch-oss:6.8.1
        environment:
            - "cluster.name=office-cluster"
            - "node.name=defn(`OFFICE_NAME')"
            - "node.master=true"
            - "node.data=true"
            - "action.auto_create_index=0"
            - "ES_JAVA_OPTS=-Xms4096m -Xmx4096m"
            - "NO_PROXY=*"
            - "no_proxy=*"
        volumes:
            - /etc/localtime:/etc/localtime:ro
        networks:
            - appnet
        user: elasticsearch
        deploy:
            placement:
                constraints:
                    - node.labels.vcac_zone!=yes
')

    defn(`OFFICE_NAME')_db_init:
        image: defn(`REGISTRY_PREFIX')smtc_db_init:latest
        environment:
            OFFICE: "defn(`OFFICE_LOCATION')"
            DBHOST: "http://ifelse(defn(`NOFFICES'),1,db,defn(`OFFICE_NAME')_db):9200"
            DBSEEDS: "ifelse(defn(`NOFFICES'),1,db,defn(`OFFICE_NAME')_db):9300"
            DBCHOST: "http://ifelse(defn(`NOFFICES'),1,db,cloud_db):9200"
            PROXYHOST: "http://defn(`OFFICE_NAME')_storage:8080"
            `SCENARIO': "defn(`SCENARIO_NAME')"
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
            placement:
                constraints:
                    - node.labels.vcac_zone!=yes
