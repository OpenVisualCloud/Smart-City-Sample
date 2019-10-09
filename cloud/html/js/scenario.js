
function update_control_options(page, map, options) {
    var control=page.data('controls');
    $.each(['heatmap','stat','preview','alert','lineinfo'], function (x, layer_name) {
        var layer_object=page.data(layer_name);
        control.removeLayer(layer_object.layer);
        if (map.hasLayer(layer_object.layer)) layer_object.layer.remove();
        if (layer_name in options) {
            control.addOverlay(layer_object.layer, layer_object.name);
            if (options[layer_name]) layer_object.layer.addTo(map);
        }
    });
}

function format_bandwidth(bandwidth) {
    var unit="b/s";
    if (bandwidth>1024) { bandwidth=bandwidth/1024; unit="Kb/s"; }
    if (bandwidth>1024) { bandwidth=bandwidth/1024; unit="Mb/s"; }
    if (bandwidth>1024) { bandwidth=bandwidth/1024; unit="Gb/s"; }
    return bandwidth>0?bandwidth.toFixed(1)+unit:"";
}

var scenarios={
    traffic: {
        name: "traffic",
        center: [45.536664,-122.960823],
        icon: {
            office: L.icon({
                iconUrl: "images/office.gif",
                iconSize: [64,64],
                iconAnchor: [32,32],
            }),
            ip_camera: L.icon({
                iconUrl: "images/camera.gif",
                iconSize: [32,32],
                iconAnchor: [16,16],
            }),
            sensor_icon: function (sensor) {
                return scenarios.traffic.icon[sensor._source.model];
            },
            sensor_icon_rotation: function (sensor) {
                return 90-sensor._source.theta;
            },
        },
        setup: function (order, page, map) {
            var layer1=L.tileLayer("images/traffic/{z}/{x}/{y}.png",{
                attribution: 'Map data &copy; <a href="https://www.openstreetmap.org/">OpenStreetMap</a> contributors, <a href="https://creativecommons.org/licenses/by-sa/2.0/">CC-BY-SA</a>',
                id: 'base'
            }).on('add', function () {
                page.data('scenario', scenarios.traffic);
                map.setView(scenarios.traffic.center,page.data('zoom'));
                update_control_options(page, map, {
                    'heatmap': true,
                    'stat': true,
                    'preview': true,
                    'alert': true,
                    'lineinfo': true,
                });
            });
            if (order==0) layer1.addTo(map).fire('add');
            page.data('controls').addBaseLayer(layer1,"Traffic Planning");
        },
        create_sensor: function (officectx, sensorctx, sensor, map) {
        },
        update_sensor: function (sensorctx, sensor) {
        },
        close_sensor: function (sensorctx) {
        }
    },
    stadium: {
        name: "stadium",
        center: [37.388085,-121.963472],
        icon: {
            office: L.icon({
                iconUrl: "images/office.gif",
                iconSize: [64,64],
                iconAnchor: [32,32],
            }),
            ip_camera: L.icon({
                iconUrl: "images/camera.gif",
                iconSize: [32,32],
                iconAnchor: [16,16],
            }),
            queue_left: L.icon({
                iconUrl: "images/queue-l.gif",
                iconSize: [90, 32],
                iconAnchor: [45, 16],
            }),
            queue_right: L.icon({
                iconUrl: "images/queue-r.gif",
                iconSize: [90, 32],
                iconAnchor: [45, 16],
            }),
            sensor_icon: function (sensor) {
                if (sensor._source.algorithm=="crowd-counting") 
                    return scenarios.stadium.icon[sensor._source.model];
                if (sensor._source.theta>=270 || sensor._source.theta<90)
                    return scenarios.stadium.icon.queue_right;
                return scenarios.stadium.icon.queue_left;
            },
            sensor_icon_rotation: function (sensor) {
                if (sensor._source.algorithm!="crowd-counting" && (sensor._source.theta>=270||sensor._source.theta<90))
                    return 270-sensor._source.theta;
                return 90-sensor._source.theta;
            },
        },
        setup: function (order, page, map) {
            var layer1=L.tileLayer('images/stadium/{z}/{x}/{y}.png',{
                tms:true
            }).on('add',function() {
                page.data('scenario', scenarios.stadium);
                map.setView(scenarios.stadium.center,page.data('zoom'));
                update_control_options(page, map, {
                    'stat': true,
                    'preview': true,
                    'alert': true,
                    'lineinfo': false,
                });
            });
            if (order==0) layer1.addTo(map).fire('add');
            page.data('controls').addBaseLayer(layer1,"Stadium Services");
        },
        create_sensor: function (officectx, sensorctx, sensor, map) {
            var add_zonemap=function () {
                var features=[]
                $.each(sensor._source.zones,function (x,v) {
                    features.push(officectx.zonedata[v]);
                });
                sensorctx.zonemap=L.geoJSON(features,{
                    onEachFeature: function (feature, layer) {
                        layer.on({
                            'dblclick': function (e) {
                                e.stopPropagation();
                                selectPage("recording",['sensor="'+sensor._id+'"',sensor._source.office]);
                            },
                            'popupopen': function () {
                                layer.unbindTooltip();
                            },
                            'popupclose': function () {
                                layer.bindTooltip(sensorctx.title);
                            },
                        });
                    },
                }).addTo(map);
            };
            if (!("zonedata" in officectx)) {
                $.getJSON("images/stadium/zonemap-"+sensor._source.office.lat+"d"+sensor._source.office.lon+".json").then(function (data) {
                    var zonedata={};
                    $.each(data,function (x,v) {
                        zonedata[v.properties.zone]=v;
                    });
                    officectx.zonedata=zonedata;
                    add_zonemap();
                });
            } else {
                add_zonemap();
            }
        },
        update_sensor: function (sensorctx, sensor) {
        },
        close_sensor: function (sensorctx) {
            sensorctx.zonemap.remove();
        }
    },
};

