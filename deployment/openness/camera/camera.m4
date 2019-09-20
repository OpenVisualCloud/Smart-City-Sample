
forloop(`OFFICEIDX',1,defn(`NOFFICES'),`dnl

    `office'defn(`OFFICEIDX')_simulated_cameras:
        image: smtc_sensor_simulation:latest
        ports:
forloop(`CAMERAIDX',1,defn(`NCAMERAS'),`dnl
            - target: eval(10000+defn(`OFFICEIDX')*1000+defn(`CAMERAIDX')*100-100)
              published: eval(10000+defn(`OFFICEIDX')*1000+defn(`CAMERAIDX')*100-100)
              protocol: tcp
              mode: host
forloop(`STEPIDX',1,20,`dnl
            - target: eval(20000+defn(`OFFICEIDX')*1000+defn(`CAMERAIDX')*100-100+defn(`STEPIDX')-1)
              published: eval(20000+defn(`OFFICEIDX')*1000+defn(`CAMERAIDX')*100-100+defn(`STEPIDX')-1)
              protocol: tcp
              mode: host
            - target: eval(20000+defn(`OFFICEIDX')*1000+defn(`CAMERAIDX')*100-100+defn(`STEPIDX')-1)
              published: eval(20000+defn(`OFFICEIDX')*1000+defn(`CAMERAIDX')*100-100+defn(`STEPIDX')-1)
              protocol: udp
              mode: host
')dnl
')dnl
        environment:
            FILES: ".mp4$$"
            `NCAMERAS': "defn(`NCAMERAS')"
            RTSP_PORT: "eval(10000+defn(`OFFICEIDX')*1000)"
            RTP_PORT: "eval(10000+defn(`OFFICEIDX')*1000)"
            PORT_STEP: "100"
        volumes:
            - /etc/localtime:/etc/localtime:ro

')dnl
