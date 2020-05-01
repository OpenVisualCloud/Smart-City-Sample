
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

#### Extending Offices

You can extend to use more offices by defining the office locations, for example:   

```
define(`traffic_office4_location',`45.528462,-122.989766')dnl
```

#### Extending Sensors (Simulated / IP Cameras)

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
        "mnth": 75.0,         # Height of the mounted camera (meter)
        "alpha": 45.0,        # Angle of camera optical axis relative to earth surface
        "fovh": 90.0,         # Horizontal field of view
        "fovv": 68.0,         # Vertical field of view
        "theta": 0.0,         # Angle of camera optical axis relative to North
        "simsn": "cams1o1c0"  # Camera identifier
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
- Download an .osm.pbf extract from [geofabrik.de](https://download.geofabrik.de) for the area you are interested in. It is recommended you download a small regional map to reduce the processing time.     
- Run the [osm-host.sh](../script/osm-host.sh) script, which will setup a local tile server on your machine ```http://localhost:8080```. The script takes the .osm.pbf file as the input argument. You can check if the map is properly rendered by looking at ```http://localhost:8080```.         
- Run the [osm-totiles.sh](../script/osm-totiles.sh) script, which will extract the tiles from the local tile server. The script takes a rectangular region as input: ```<lon_min> <lon_max> <lat_min> <lat_max>```. This region will be your observable scenario map. The extracted tiles should be copied under [images/traffic](../cloud/html/images/traffic). You can delete any old tiles under [images/traffic](../cloud/html/images/traffic).   
- Kill the local tile server: ```docker ps``` and ```docker kill```. We don't need it any more.   
- Modify [scenario.js](../cloud/html/js/scenario.js) with the new display center location.   

Rebuild the sample. You are good to go.  

### Stadium Scenario

The stadium scenario includes the following modes: entrance and service-point people counting and seating-area crowd counting. The following sub-sections describe extension possibilities.  

#### Extending Offices

Modify the following files to update or extend office defintions:   
- [sensor-info.m4](../maintenance/db-init/sensor-info.m4)
- [sensor-info.json](../maintenance/db-init/sensor-info.json)
- [zonemap-xxx.json](../cloud/html/images/stadium/zonemap-37.39856d-121.94866.json)

#### Extending Entrances/Service Points

The sensor provisioning information is described in [sensor-info.json](../maintenance/db-init/sensor-info.json). An example is as follows:   

```
...
{
    "scenario": "stadium",
    "address": "National Stadium",  # Office friendly name
    "location": {
        "lat": 37.39856,            # Office location
        "lon": -121.94866           # Office location
    },
    "sensors": [{
        "address": "East Gate",     # Sensor friendly name
        "location": {
            "lat": 37.38813,        # Sensor location
            "lon": -121.94370       # Sensor location
        },
        "algorithm": "entrance-counting",  # Analytic algorithm to associate with
        "theta": 90.0,              # The rotation angle with 0 degree facing North
        "simsn": "cams2o1c0"        # Camera identifier
    },{
        ...
    }]
}
...
```

Modify [sensor-info.json](../maintenance/db-init/sensor-info.json) as needed to change or add more entrances/service points.  

#### Extending Seating Zones

Crowd-counting requires the following transformations (and thus parameters that you must provide as part of the provisioning information):   
- **Image to Zone**: A camera may point to a zone or multiple zones of seats. The mapping from image pixels to zones are described in [sensor-info.json](../maintenance/db-init/sensor-info.json). An example is as follows:  

```
    {
        "address": "East Wing",         # Sensor friendly name
        "location": {
            "lat": 37.38865,            # Sensor location
            "lon": -121.95405           # Sensor location
        },
        "algorithm": "crowd-counting",  # Analytics algorithm to be associated with 
        "theta": 270.0,                 # Sensor rotation with 0 degree facing North
        "zones": [0],                   # Zone information
        "zonemap": [{
            "zone": 0,                  # 2D polygons to describe the zone boundary
            "polygon": [[0,0],[1023,0],[1023,1023],[0,1023],[0,0]]
        }],
        "simsn": "cams2o1w0"            # Camera identifier
    }
```

- **Zone to Map**: After analytics, to display the estimated seat occupencies on the scenario map, the mapping from zone to map location is required. See [zonemap-xxx.json](../cloud/html/images/stadium/zonemap-37.39856d-121.94866.json):   

```
[{
  "type": "Feature",
  "properties": {
    "office": {
       "lat": 37.39856,           # Office location
       "lon": -121.94866          # Office location
    },
    "zone": 2,                    # Zone index
    "name": "North Wing"          # Office friendly name
  },
  "geometry": {
    "type": "Polygon",
    "coordinates": [[             # Polygons to describe the zone boundary
      [ -121.97061, 37.39661 ],
      [ -121.97061, 37.39581 ],
      [ -121.97011, 37.39581 ],
      [ -121.97011, 37.39506 ],
      [ -121.96880, 37.39506 ],
      [ -121.96880, 37.39428 ],
      [ -121.95647, 37.39428 ],
      [ -121.95647, 37.39504 ],
      [ -121.95545, 37.39504 ],
      [ -121.95545, 37.39581 ],
      [ -121.95444, 37.39581 ],
      [ -121.95446, 37.39661 ],
      [ -121.97061, 37.39661 ]
    ]]
  }
}]
```

#### Extending Scenario Map

A stadium scenario map is a 2D image transformed to the Earth coordinates. First draw a stadium map using any image editor. SVG-type image editor is preferred as we need to scale the image later. See [Stadium Map.vsdx](asset/Stadium%20Map.vsdx) as an example. The image must be a square image and the size not larger than ```12960x12960```. Save it as a PNG file.   

Run the [png-totiles.sh](../script/png-totiles.sh) script as follows:    
```
cd cloud/html/images
../../../script/png-totiles.sh stadium <lon_min> <lon_max> <lat_min> <lat_max> stadium.png .
```
where ```<lon_min>...<lat_max>``` are the square region coordinates.  

The script will generate the map tiles under [cloud/html/images/stadium](../cloud/html/images/stadium), and a geo-wrapped image ```stadium_modified.tiff```. 

The geo-wrapped image ```stadium_modified.tiff``` can be used to obtain location coordinates for offices, sensors, and seats. You can use [QGIS](https://www.qgis.org/en/site/index.html) or similar software to import the image and then examine the coordinates. The following files defines the office, sensor, and seats geo locations:   

- [sensor-info.m4](../maintenance/db-init/sensor-info.m4)   
- [sensor-info.json](../maintenance/db-init/sensor-info.json)   
- [zonemap-xxx.json](../cloud/html/images/stadium/zonemap-37.39856d-121.94866.json)  
- [scenario.js](../cloud/html/js/scenario.js)   

The geo-wrapped image is not directly used in the sample. You should delete it before building the sample.   

### See Also

- [Extending with IP Cameras](../sensor/README.md)   

