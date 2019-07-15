The sample scans the specified IP block for any IP cameras. If found, they will be registered to the database and be invoked by analytic instances for streaming.

### Sensor Simulation

The sample will simulate camera feeds if there is any MP4 files under the [../volume/simulated](../volume/simulated) directory. The MP4 files must be encoded with H.264 baseline/main profile and AAC if there is audio. If you change any files under [../volume/simulated](../volume/simulated), please restart the sample services.    

### ONVIF Camera Discovery

The sample implements the ONVIF protocol to discover IP cameras on the specified IP range and port range. To activate the ONVIF camera discovery, modify the following service block in the [docker-compose.yml](../deployment/docker-swarm/docker-compose.yml) file, and restart the sample services:     

```
    onvif-discovery:
        image: smtc_onvif_discovery:latest
        environment:
            IP_SCAN_RANGE: '192.168.1.0/24'
            PORT_SCAN_RANGE: '0-65535'
            OFFICE: '45.543797,-122.962038'
            DISTANCE: 2
            ANGLEOFFSET: 15
        deploy:
            replicas: 1
        restart: always
```
