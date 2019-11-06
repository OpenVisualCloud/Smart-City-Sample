
This document describes how to extend the sensors, offices and scenario maps for the Smart-City sample.    

### Traffic Scenario

The sensors and offices data are defined in the following files:   

- [sensor-info.m4](../maintenance/db-init/sensor-info.m4)
- [sensor-info.json](../maintenance/db-init/sensor-info.json)
- [scenario.js](../cloud/html/js/scenario.js)

[sensor-info.m4](../maintenance/db-init/sensor-info.m4) is used in the deployment scripts. Only the office location information is included as follows:   

```
define(`traffic_office1_location',`45.539626,-122.929569')dnl
define(`traffic_office2_location',`45.524460,-122.960475')dnl
define(`traffic_office3_location',`45.543645,-122.984178')dnl
```

You can extend to use more offices by defining the office locations, for example:   

```
define(`traffic_office4_location',`45.528462,-122.989766')dnl
```

For each office (and scenario), [sensor-info.json](../maintenance/db-init/sensor-info.json) defines the camera provisioning information. Any detected cameras (whether simulated or IP cameras) will be matched against this provisioning information, format as follows:   

```
[{
    "scenario": "traffic",
    "address": "Dawson Creek",    # Office friendly name
    "location": {
        "lat": 45.539626,         # Office location
        "lon": -122.929569        # Office location
    },
    "sensors": [{
        "address": "Shute & Dawson Creek",  # Sensor location friendly name
        "location": {
            "lat": 45.544223,               # Sensor location
            "lon": -122.926128              # Sensor location
        },
        "algorithm": "object-detection",    # The analytic algorithm to run
        "mnth": 75.0,      # Height of the mounted camera (meter)
        "alpha": 45.0,     # Angle of camera optical axis relative to earth surface
        "fovh": 90.0,      # Horizontal field of view
        "fovv": 68.0,      # Vertical field of view
        "theta": 0.0,      # Angle of camera optical axis relative to North
        "simsn": "cams1o1c0"    # cams1o<office-number>c<camera-id>
    },{
       ...
    }],
...
}]
```

You can modify or add new entries that represent new simulated cameras or IP cameras. If you plan to extend with IP cameras, please see [Extending IP Cameras](../sensor/README.md) for how to discover the camera identifiers and create entries of the IP camera provisioning information.   

[scenario.js](../cloud/html/js/scenario.js) is used in the sample UI. Normally, you don't need to modify it, unless you want to move the center of the scenario map. Modify the display center as needed.

#### Extending the Scenario Map

The scenario map is currently limited to portion of Hillsboro, Oregon, USA. You can extend it to any location you like as follows:   
- Download an .osm.pbf extract from [geofabrik.de](https://download.geofabrik.de) for the area you are interested in.    
- Run the [osm_host.sh](../script/osm_host.sh) script, which will setup a local tile server on your machine http://localhost:8080. The script takes a single command-line argument: the .osm.pbf file.     
- Run the [osm_totiles.sh](../script/osm_totiles.sh) script, which will extract the tiles from the local tile server. The script takes a rectangular region as input: ```<lon_min> <lon_max> <lat_min> <lat_max>```. This region will be your observable scenario map. The extracted tiles should be copied to be under [images/traffic](../cloud/html/images/traffic).  
- Kill the local tile server: ```docker ps``` && ```docker kill```. We don't need it any more.   
- Modify [scenario.js](../cloud/html/js/scenario.js) with the new display center location.   

Rebuild the sample. You are good to go.  

### Stadium Scenario: Entrance People Counting

TODO

### Stadium Scenario: Seat Crowd Counting

TODO


