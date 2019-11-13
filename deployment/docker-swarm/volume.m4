
volumes:
    ifelse(eval(defn(`NOFFICES')>1),1,cloud_esdata,esdata):
        driver: local
    cloud_stdata:
        driver: local
forloop(`SCENARIOIDX',1,defn(`NSCENARIOS'),`dnl
forloop(`OFFICEIDX',1,defn(`NOFFICES'),`dnl
include(office.m4)dnl
ifelse(index(defn(`SCENARIO'),defn(`SCENARIO_NAME')),-1,,`dnl
ifelse(defn(`OFFICE_LOCATION'),`',,`dnl
    defn(`OFFICE_NAME')_esdata:
        driver: local
    defn(`OFFICE_NAME')_stdata:
        driver: local
')')')')
