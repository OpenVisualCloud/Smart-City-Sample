
    ifelse(eval(defn(`NOFFICES')>1),1,cloud_db,db):
        image: docker.elastic.co/elasticsearch/elasticsearch-oss:6.8.1
        environment:
ifelse(eval(defn(`NOFFICES')>1),1,`dnl
            - "cluster.name=db-cluster"
            - "node.name=cloud_db"
            - "node.master=true"
            - "node.data=true"
            - "node.attr.zone=cloud"
            - "ES_JAVA_OPTS=-Xms2048m -Xmx2048m"
',`dnl
            - "discovery.type=single-node"
')dnl
            - "action.auto_create_index=0"
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
