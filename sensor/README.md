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
            PORT_SCAN_RANGE: '554-8554'
            OFFICE: '45.539626,-122.929569'
            LOCATION: '45.544223,-122.926128,45.546249,-122.932145,45.538971,-122.939726'
