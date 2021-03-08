
    ifelse(defn(`NOFFICES'),1,db,cloud_db):
        image: docker.elastic.co/elasticsearch/elasticsearch-oss:6.8.13
        environment:
ifelse(defn(`NOFFICES'),1,`dnl
            - "discovery.type=single-node"
',`dnl
            - "cluster.name=cloud-cluster"
            - "node.name=cloud_db"
            - "node.master=true"
            - "node.data=true"
            - "ES_JAVA_OPTS=-Xms2048m -Xmx2048m"
')dnl
            - "action.auto_create_index=0"
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
