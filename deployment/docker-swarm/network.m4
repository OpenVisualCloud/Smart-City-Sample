
networks:
    db_net:
    cloud_net:
forloop(`id',1,defn(`NOFFICES'),`dnl
ifdef(`location_office'defn(`id'),`dnl
    `office'defn(`id')_net:
        attachable: true
    `camera'defn(`id')_net:
        attachable: true
')dnl
')
