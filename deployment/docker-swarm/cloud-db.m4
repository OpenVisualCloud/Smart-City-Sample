
    ifelse(eval(defn(`NOFFICES')>1),1,cloud_db,db):
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
            - "ES_JAVA_OPTS=-Xms2048m -Xmx4096m"
            - "NO_PROXY=*"
            - "no_proxy=*"
        volumes:
            - /etc/localtime:/etc/localtime:ro
            - ifelse(eval(defn(`NOFFICES')>1),1,cloud_esdata,esdata):/usr/share/elasticsearch/data:rw
ifelse(defn(`PLATFORM'),`VCAC-A',`dnl
        networks:
            - default_net
')dnl
        deploy:
            placement:
                constraints:
                    - node.role==manager
