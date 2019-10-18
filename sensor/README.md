
The Smart City sample scans the specified IP block for any cameras. If found, they will be registered to the database and be invoked by analytic instances for streaming.

### Sensor Simulation

The sample implemented camera simulation to facilitate evalaution. Camera simulation requires that you have a dataset to simulate camera feeds. The build script includes a sample clip (to be downloaded after accepting the license terms.)

If you plan to use your own dataset, put the files under the [simulation](simulation) directory. The dataset must be a set of MP4 files, encoded with H.264 (configuration: baseline, closed-GOP and no-B-frames) and AAC.

If unsure, it is recommended that you transcode your dataset with FFmpeg:

```
ffmpeg -i <source>.mp4 -c:v libx264 -profile:v baseline -x264-params keyint=30:bframes=0 -c:a aac -ss 0 <target>.mp4
```

### Extending to IP Cameras

The sample implements the ONVIF protocol to discover IP cameras on the specified IP range. Do the following to add IP cameras to the sample:   

#### (1) Finding Camera IDs

To uniquely identify a camera, we need to define a camera ID. This is usually the camera serial number (1st choice) or the MAC address of the network interface (2nd choice if serial number is missing from probing).  

Scan the camera IP range as follows:
```
PORT_SCAN='-p80-65535 192.168.1.0/24' make discover
```

where ```PORT_SCAN``` specifies the ```nmap``` command line arguments. The camera network is ```192.168.1.0/24``` and the port range is ```80-65535```. The output is similar to the following lines:    

```
...
  "device": {
    "Manufacturer": "LOREX",
    "Model": "LNB8973B",
    "FirmwareVersion": "2.460.0001.5.R, Build Date 2017-08-11",
    "SerialNumber": "ND021808019141",
    "HardwareId": "1.00"
  },
  "networks": [
    {
      "Name": "eth0",
      "HwAddress": "00:1f:54:2d:3d:1b",
      "MTU": 1500
    }
  ],
...
```

Note that the sample uses a predefined username and password for camera authentication. See [```probe_camera_info```](../sensor/discovery/discover.py) for details.  

#### (2) Provisioning Cameras

Provisioning is a process of associating a set of application-specific parameters to a camera, for example, the GPS location, field of view, direction and positioning transformation. Developing provisioning tools is outside the sample scope. As a workaround, the sample stores the provisioning information at [sensor-info.json](../maintenance/db-init/sensor-info.json) and uses it to initialize the database.   

The provisioning information is scenario specific. The ```traffic``` scenario parameters are as follows:
```
...
        "address": "Tendem Way",
        "location": {
            "lat": 45.5415,
            "lon": -122.9227
        },
        "algorithm": "object-detection",
        "mnth": 75.0,
        "alpha": 45.0,
        "fovh": 90.0,
        "fovv": 68.0,
        "theta": 0.0,
        "simsn": "cams1o1c7"
...
```
The ```stadium``` scenario parameters are as follows:
```
...
        "address": "South East Wing",
        "location": {
            "lat": 37.38369,
            "lon": -121.95448
        },
        "algorithm": "crowd-counting",
        "theta": 225.0,
        "zones": [7],
        "zonemap": [{
            "zone": 7,
            "polygon": [[0,0],[1023,0],[1023,1023],[0,1023],[0,0]]
        }],
        "simsn": "cams2o1w7"
...
```

In above provisioning parameters, the ```simsn``` fields identify simulated cameras. Replace those with the discovered camera IDs. For example, the following parameters associate the ```South East Wing``` or ```zone 7``` with the IP camera, whose serial number is ```ND021808019141```.   
```
...
        "address": "South East Wing",
        "location": {
            "lat": 37.38369,
            "lon": -121.95448
        },
        "algorithm": "crowd-counting",
        "theta": 225.0,
        "zones": [7],
        "zonemap": [{
            "zone": 7,
            "polygon": [[0,0],[1023,0],[1023,1023],[0,1023],[0,0]]
        }],
        "device": { 
            "SerialNumber": "ND021808019141"
        }
...
```

#### (3) Enabling Discovering Service

Enable the ```ipcamera-discovery``` service in the deployment scripts ([camera-discovery.m4](../deployment/docker-swarm/camera-discovery.m4) for docker compose or docker swarm and [camera-discovery.yaml.m4](../deployment/kubernetes/camera-discovery.yaml.m4) for kubernetes) by replacing ```replicas: 0``` with ```replicas: 1```.   

Restart the sample. Your IP camera(s) should show up in the sample UI.      

