
volumes:
    ifelse(eval(defn(`NOFFICES')>1),1,cloud_esdata,esdata):
        driver: local
forloop(`office_idx',1,defn(`NOFFICES'),`dnl
    `office'defn(`office_idx')_esdata:
        driver: local
    `office'defn(`office_idx')_andata:
        driver: local
    `office'defn(`office_idx')_stdata:
        driver: local
')dnl
