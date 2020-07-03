
The Smart City sample scans the specified IP block for any cameras. If found, they will be registered to the database and be invoked by analytic instances for streaming.

### Sensor Simulation

The sample implemented camera simulation to facilitate evalaution. Camera simulation requires that you have a dataset to simulate camera feeds. The build script includes a sample clip (to be downloaded after accepting the license terms.)

If you plan to use your own dataset, put the files under the [simulation](simulation) directory. Rename them to follow the convention of ```<dataset-name>_<scenario>.mp4```. The dataset must be a set of MP4 files, encoded with H.264 (configuration: baseline, closed-GOP and no-B-frames) and AAC.   

If unsure, it is recommended that you transcode your dataset with FFmpeg:

```
ffmpeg -i <source>.mp4 -c:v libx264 -profile:v baseline -x264-params keyint=30:bframes=0 -c:a aac -ss 0 <target>.mp4
```

### Extending to IP Cameras

The sample implements the ONVIF protocol to discover IP cameras on the specified IP range. Do the following to add IP cameras to the sample:   

#### (1) Uniquely Identifying an IP Camrea

Assume an IP camera can be on and off during the streaming cycles, we need to define a way to uniquely identify an IP camera (so that we can associate any [provisioning](#2-provisioning-cameras) parameters to the camera.)   

If the IP address of an IP camera is statically assigned, then the pair of the assigned IP address and the camera RTSP port can be the unique identifier. 

If the IP address is assigned through DHCP, then we need to use the ONVIF protocol to locate the camera serial number or the MAC address. Either one can be the unique identifier. Use the following script to scan the network for IP cameras:  

```
read && PORT_SCAN='-p T:80-65535 192.168.1.0/24' PASSCODE=$REPLY make discover
```

where `PORT_SCAN` specifies the `nmap` command line arguments. The camera network is `192.168.1.0/24` and the port range is `80-65535`. At the prompt, please enter the passcode of the IP camera as `username:password`. The output is similar to the following lines:    

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

#### (2) Provisioning Cameras

Provisioning is a process of associating a set of application-specific parameters to a camera, for example, the GPS location, field of view, direction and positioning transformation. Developing provisioning tools is outside the sample scope. As a workaround, the sample stores the provisioning information in [sensor-info.json](../maintenance/db-init/sensor-info.json) and uses it to initialize the database.   

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

In above provisioning parameters, the `simsn` fields identify simulated cameras. Replace those with the IP camera [unique identifiers](#1-Uniquely-Identifying-an-IP-Camrea).  

For example, the following parameters associate the ```South East Wing``` or ```zone 7``` with an IP camera, whose serial number is ```ND021808019141```,  
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
        "passcode": "admin:admin"
        "ip": "192.168.1.0/16",
        "device": { 
            "SerialNumber": "ND021808019141"
        },
...
```

or with statically allocated IP address(es) and the RTSP ports.     
```
...
        "passcode": "admin:admin",
        "ip": "192.168.1.114",
        "port": [ 80, 9988 ]
...
```

where `passcode` specifies the camera username and password; `ip` can be either a specific IP address `192.168.1.114` or an IP address range such as `192.168.1.0/24`; and `port` is a list of the camera RTSP ports.    

---

It is recommended that you always specify an IP address range to be associated with `passcode`. Certain IP cameras may lock up for a period of time if fed with a wrong passcode.   

---

#### (3) Enabling the Discovering Service

Enable the IP camera discovering service by configuring ```DISCOVER_IP_CAMERA``` to ```true``` in [Docker swarm/office.m4](../deployment/docker-swarm/office.m4), [Kubernetes/office.m4](../deployment/kubernetes/yaml/office.m4), or [Kubernetes Helm/values.yaml.m4](../deployment/kubernetes/helm/smtc/values.yaml.m4).

--- 

Due to Kubernetes limitation, if IP camera is enabled, the discovering service and the analytics instances will run on the host network for reliably receiving RTP streams.   

---

If you enable more than 1 office, addtionally check the ```IP_CAMERA_NETWORK``` definition. The default value assumes that each office occupies a block in the ```192.168.x.0/24``` network. Modify as necessary. Also, make sure that the worker node that runs the IP camera discovering service can access to the specified network.     

Restart the sample. Your IP camera(s) should show up in the sample UI.      

