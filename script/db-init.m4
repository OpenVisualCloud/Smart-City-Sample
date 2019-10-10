include(../../script/forloop.m4)
include(../../script/sensor-info.m4)
forloop(`SCENARIOIDX',1,defn(`NSCENARIOS'),`dnl
forloop(`OFFICEIDX',1,defn(`NOFFICES'),`dnl
forloop(`CAMERAIDX',1,defn(`NCAMERAS'),`dnl
define(`OFFICE_LOCATION',defn(`scenario'defn(`SCENARIOIDX')`_office'defn(`OFFICEIDX')_location))dnl
define(`CAMERA_NAME',`defn(`scenario'defn(`SCENARIOIDX')`_office'defn(`OFFICEIDX')`_camera'defn(`CAMERAIDX')')dnl
define(`CAMERA_LOCATION',defn(`scenario'defn(`SCENARIOIDX')`_office'defn(`OFFICEIDX')`_camera'defn(`CAMERAIDX')_location)dnl
ifdef(defn(`CAMERA_NAME')_location,`dnl
{
    "office": {
        "lat": patsubst(defn(`OFFICE_LOCATION'),`,.*',`'),
        "lon": patsubst(defn(`OFFICE_LOCATION'),`[-.0-9]+, ',`')
    },
    "location": {
        "lat": patsubst(defn(`CAMERA_LOCATION'),`,.*',`'),
        "lon": patsubst(defn(`CAMERA_LOCATION'),`[-.0-9]+, ',`')
    },
    "address": "defn(defn(`CAMERA_NAME')_address)",
    "theta": defn(defn(`CAMERA_NAME')_theta),
    "alpha": 45.0,
    "mnth": 75.0,
    "fovh": 90.0,
    "fovv": 68.0,
    "zone": [defn(defn(`CAMERA_NAME')_zone)],
},
')')')')dnl
