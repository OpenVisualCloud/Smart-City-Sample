include(platform.m4)

ifelse(defn(`SCENARIO_NAME'),`traffic',`
    defn(`OFFICE_NAME')_analytics_traffic:
        image: PLATFORM_IMAGE(defn(`REGISTRY_PREFIX')`smtc_analytics_object_'defn(`PLATFORM_SUFFIX')`_'defn(`FRAMEWORK'):latest)
        volumes:
            - /etc/localtime:/etc/localtime:ro
PLATFORM_VOLUME_EXTRA()dnl
        environment:
            PLATFORM_ENV(OFFICE): "defn(`OFFICE_LOCATION')"
            PLATFORM_ENV(DBHOST): "http://ifelse(eval(defn(`NOFFICES')>1),1,defn(`OFFICE_NAME')_db,db):9200"
            PLATFORM_ENV(MQTTHOST): "defn(`OFFICE_NAME')_mqtt"
            PLATFORM_ENV(EVERY_NTH_FRAME): 6
            PLATFORM_ENV(``SCENARIO''): "defn(`SCENARIO_NAME')"
            PLATFORM_ENV(STHOST): "http://defn(`OFFICE_NAME')_storage:8080/api/upload"
            PLATFORM_ENV(PIPELINE_VERSION): 2
            PLATFORM_ENV(``NETWORK_PREFERENCE''): "{\"defn(`PLATFORM_DEVICE')\":\"defn(`NETWORK_PREFERENCE')\"}"
            PLATFORM_ENV(NO_PROXY): "*"
            PLATFORM_ENV(no_proxy): "*"
PLATFORM_ENV_EXTRA()dnl
        networks:
            - appnet
        deploy:
            replicas: defn(`NANALYTICS')
            placement:
                constraints:
                    - PLATFORM_ZONE()
')

ifelse(defn(`SCENARIO_NAME'),`stadium',`
    defn(`OFFICE_NAME')_analytics_entrance:
        image: PLATFORM_IMAGE(defn(`REGISTRY_PREFIX')`smtc_analytics_entrance_'defn(`PLATFORM_SUFFIX')`_'defn(`FRAMEWORK'):latest)
        volumes:
            - /etc/localtime:/etc/localtime:ro
PLATFORM_VOLUME_EXTRA()dnl
        environment:
            PLATFORM_ENV(OFFICE): "defn(`OFFICE_LOCATION')"
            PLATFORM_ENV(DBHOST): "http://ifelse(eval(defn(`NOFFICES')>1),1,defn(`OFFICE_NAME')_db,db):9200"
            PLATFORM_ENV(MQTTHOST): "defn(`OFFICE_NAME')_mqtt"
            PLATFORM_ENV(EVERY_NTH_FRAME): 6
            PLATFORM_ENV(``SCENARIO''): "defn(`SCENARIO_NAME')"
            PLATFORM_ENV(STHOST): "http://defn(`OFFICE_NAME')_storage:8080/api/upload"
            PLATFORM_ENV(``NETWORK_PREFERENCE''): "{\"defn(`PLATFORM_DEVICE')\":\"defn(`NETWORK_PREFERENCE')\"}"
            PLATFORM_ENV(NO_PROXY): "*"
            PLATFORM_ENV(no_proxy): "*"
PLATFORM_ENV_EXTRA()dnl
        networks:
            - appnet
        deploy:
            replicas: defn(`NANALYTICS3')
            placement:
                constraints:
                    - PLATFORM_ZONE()

    defn(`OFFICE_NAME')_analytics_crowd:
        image: PLATFORM_IMAGE(defn(`REGISTRY_PREFIX')`smtc_analytics_crowd_'defn(`PLATFORM_SUFFIX')`_'defn(`FRAMEWORK'):latest)
        volumes:
            - /etc/localtime:/etc/localtime:ro
PLATFORM_VOLUME_EXTRA()dnl
        environment:
            PLATFORM_ENV(OFFICE): "defn(`OFFICE_LOCATION')"
            PLATFORM_ENV(DBHOST): "http://ifelse(eval(defn(`NOFFICES')>1),1,defn(`OFFICE_NAME')_db,db):9200"
            PLATFORM_ENV(MQTTHOST): "defn(`OFFICE_NAME')_mqtt"
            PLATFORM_ENV(EVERY_NTH_FRAME): "6"
            PLATFORM_ENV(``SCENARIO''): "defn(`SCENARIO_NAME')"
            PLATFORM_ENV(STHOST): "http://defn(`OFFICE_NAME')_storage:8080/api/upload"
            PLATFORM_ENV(``NETWORK_PREFERENCE''): "{\"defn(`PLATFORM_DEVICE')\":\"defn(`NETWORK_PREFERENCE')\"}"
            PLATFORM_ENV(NO_PROXY): "*"
            PLATFORM_ENV(no_proxy): "*"
PLATFORM_ENV_EXTRA()dnl
        networks:
            - appnet
        deploy:
            replicas: defn(`NANALYTICS2')
            placement:
                constraints:
                    - PLATFORM_ZONE()

    defn(`OFFICE_NAME')_analytics_svcq:
        image: PLATFORM_IMAGE(defn(`REGISTRY_PREFIX')`smtc_analytics_object_'defn(`PLATFORM_SUFFIX')`_'defn(`FRAMEWORK'):latest)
        volumes:
            - /etc/localtime:/etc/localtime:ro
PLATFORM_VOLUME_EXTRA()dnl
        environment:
            PLATFORM_ENV(OFFICE): "defn(`OFFICE_LOCATION')"
            PLATFORM_ENV(DBHOST): "http://ifelse(eval(defn(`NOFFICES')>1),1,defn(`OFFICE_NAME')_db,db):9200"
            PLATFORM_ENV(MQTTHOST): "defn(`OFFICE_NAME')_mqtt"
            PLATFORM_ENV(EVERY_NTH_FRAME): 6
            PLATFORM_ENV(``SCENARIO''): "defn(`SCENARIO_NAME')"
            PLATFORM_ENV(STHOST): "http://defn(`OFFICE_NAME')_storage:8080/api/upload"
            PLATFORM_ENV(PIPELINE_VERSION): 2
            PLATFORM_ENV(``NETWORK_PREFERENCE''): "{\"defn(`PLATFORM_DEVICE')\":\"defn(`NETWORK_PREFERENCE')\"}"
            PLATFORM_ENV(NO_PROXY): "*"
            PLATFORM_ENV(no_proxy): "*"
PLATFORM_ENV_EXTRA()dnl
        networks:
            - appnet
        deploy:
            replicas: defn(`NANALYTICS')
            placement:
                constraints:
                    - PLATFORM_ZONE()
')
