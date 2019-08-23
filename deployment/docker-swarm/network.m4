
networks:
    db_net:
    cloud_net:
forloop(`id',1,defn(`NOFFICES'),`dnl
ifdef(`location_office'defn(`id'),`dnl
    `office'defn(`id')_net:
    `camera'defn(`id')_net:
')dnl
')
