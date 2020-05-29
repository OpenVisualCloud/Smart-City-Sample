
function update_control_options(page, map, options) {
    var control=page.data('controls');
    $.each(['heatmap','stat','preview','alert','lineinfo'], function (x, layer_name) {
        var layer_object=page.data(layer_name);
        layer_object.layer.clearLayers();
        control.removeLayer(layer_object.layer);
        map.removeLayer(layer_object.layer);
        if (layer_name in options) {
            control.addOverlay(layer_object.layer, layer_object.name);
            if (options[layer_name]) layer_object.layer.addTo(map);
        }
    });
}

function format_bandwidth(bandwidth) {
    var unit=text["b/s"];
    if (bandwidth>1024) { bandwidth=bandwidth/1024; unit=text["kb/s"]; }
    if (bandwidth>1024) { bandwidth=bandwidth/1024; unit=text["mb/s"]; }
    if (bandwidth>1024) { bandwidth=bandwidth/1024; unit=text["gb/s"]; }
    return bandwidth>0?bandwidth.toFixed(1)+unit:"";
}

var scenarios={
    traffic: {
        name: "traffic",
        center: [45.536664,-122.960823],
        icon: {
            office: {
                online: L.icon({
                    iconUrl: "images/office-online.gif",
                    iconSize: [64,64],
                    iconAnchor: [32,32],
                }),
                offline: L.icon({
                    iconUrl: "images/office-offline.gif",
                    iconSize: [64,64],
                    iconAnchor: [32,32],
                }),
            },
            ip_camera: {
                idle: L.icon({
                    iconUrl: "images/camera-idle.gif",
                    iconSize: [32,32],
                    iconAnchor: [16,16],
                }),
                streaming: L.icon({
                    iconUrl: "images/camera-streaming.gif",
                    iconSize: [32,32],
                    iconAnchor: [16,16],
                }),
                disconnected: L.icon({
                    iconUrl: "images/camera-disconnected.gif",
                    iconSize: [32,32],
                    iconAnchor: [16,16],
                }),
            },
            sensor_icon: function (sensor, online) {
                return scenarios.traffic.icon[sensor._source.model][online?sensor._source.status:"disconnected"];
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
                setTimeout(function () { /* outof callback */
                    update_control_options(page, map, {
                        'heatmap': true,
                        'stat': true,
                        'preview': true,
                        'alert': true,
                        'lineinfo': true,
                    });
                },10);
                page.data('scenario', scenarios.traffic);
                map.setView(scenarios.traffic.center,page.data('zoom'));
            });
            if (order==0) layer1.addTo(map).fire('add');
            page.data('controls').addBaseLayer(layer1,text["traffic planning"]);
        },
        create_sensor: function (officectx, sensorctx, sensor, page, map) {
            stats.create(sensorctx, sensor, page, map, function (chart_div) { return null; });
            heatmap.create(sensorctx, sensor._source.location);

            sensorctx.update_sensor=function (sensor) {
                var stat_layer=page.data('stat').layer;
                if (map.hasLayer(stat_layer)) {
                    apiHost.histogram("analytics",'sensor="'+sensor._id+'" and '+settings.stats_query(),settings.stats_histogram(),25,sensor._source.office).then(function (data) {
                        stats.update(stat_layer, sensorctx, map.getZoom(), sensor, data, null);
                    }).catch(function () {
                        stats.update(stat_layer, sensorctx, map.getZoom(), sensor, {}, null);
                    });
                }

                /* show heatmap */
                var heatmap_layer=page.data('heatmap').layer;
                if (map.hasLayer(heatmap_layer))
                    heatmap.update(heatmap_layer, sensorctx, map.getZoom(), sensor);
            };
            sensorctx.close_sensor=function () {
                stats.close(sensorctx);
                heatmap.close(sensorctx);
            };
        },
    },
    stadium: {
        name: "stadium",
        center: [37.388085,-121.963472],
        icon: {
            office: {
                online: L.icon({
                    iconUrl: "images/office-online.gif",
                    iconSize: [64,64],
                    iconAnchor: [32,32],
                }),
                offline: L.icon({
                    iconUrl: "images/office-offline.gif",
                    iconSize: [64,64],
                    iconAnchor: [32,32],
                }),
            },
            ip_camera: {
                idle: L.icon({
                    iconUrl: "images/camera-idle.gif",
                    iconSize: [32,32],
                    iconAnchor: [16,16],
                }),
                streaming: L.icon({
                    iconUrl: "images/camera-streaming.gif",
                    iconSize: [32,32],
                    iconAnchor: [16,16],
                }),
                disconnected: L.icon({
                    iconUrl: "images/camera-disconnected.gif",
                    iconSize: [32,32],
                    iconAnchor: [16,16],
                }),
            },
            queue: {
                left: {
                    idle: L.icon({
                        iconUrl: "images/queue-l-idle.gif",
                        iconSize: [90, 32],
                        iconAnchor: [45, 16],
                    }),
                    streaming: L.icon({
                        iconUrl: "images/queue-l-streaming.gif",
                        iconSize: [90, 32],
                        iconAnchor: [45, 16],
                    }),
                    disconnected: L.icon({
                        iconUrl: "images/queue-l-disconnected.gif",
                        iconSize: [90, 32],
                        iconAnchor: [45, 16],
                    }),
                },
                right: {
                    idle: L.icon({
                        iconUrl: "images/queue-r-idle.gif",
                        iconSize: [90, 32],
                        iconAnchor: [45, 16],
                    }),
                    streaming: L.icon({
                        iconUrl: "images/queue-r-streaming.gif",
                        iconSize: [90, 32],
                        iconAnchor: [45, 16],
                    }),
                    disconnected: L.icon({
                        iconUrl: "images/queue-r-disconnected.gif",
                        iconSize: [90, 32],
                        iconAnchor: [45, 16],
                    }),
                },
            },
            sensor_icon: function (sensor, online) {
                var status=online?sensor._source.status:"disconnected";
                if (sensor._source.algorithm=="crowd-counting") 
                    return scenarios.stadium.icon[sensor._source.model][status];
                var lr=(sensor._source.theta>=270 || sensor._source.theta<90)?"right":"left";
                return scenarios.stadium.icon.queue[lr][status];
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
                setTimeout(function () { /* outof callback */
                    update_control_options(page, map, {
                        'stat': true,
                        'preview': true,
                        'alert': true,
                        'lineinfo': false,
                    });
                },10);
                page.data('scenario', scenarios.stadium);
                map.setView(scenarios.stadium.center,page.data('zoom'));
            });
            if (order==0) layer1.addTo(map).fire('add');
            page.data('controls').addBaseLayer(layer1,text["stadium services"]);
        },
        create_sensor: function (officectx, sensorctx, sensor, page, map) {
            stats.create(sensorctx, sensor, page, map, function (chart_div) {
                if (sensor._source.algorithm=="crowd-counting") {
                    sensorctx.zonemap=L.geoJSON(null,{
                        onEachFeature: function (feature, layer) {
                            layer.bindPopup(chart_div,{ maxWidth:"auto",maxHeight:"auto" });
                        },
                    });
                    return sensorctx.zonemap;
                }
                return null;
            });
            sensorctx.update_sensor=function (sensor) {
                var stat_layer=page.data('stat').layer;
                if (map.hasLayer(stat_layer)) {
                    var fields=[], iconloc=null;
                    if (sensor._source.algorithm=="object-detection") {
                        fields.push("nobjects");
                    } else if (sensor._source.algorithm=="entrance-counting" || sensor._source.algorithm=="svcq-counting") {
                        fields.push("count.people");
                    } else if (sensor._source.algorithm=="crowd-counting") {
                        iconloc=sensorctx.zonemap.getBounds().getCenter();
                        $.each(sensor._source.zones,function (x,v) {
                            fields.push("count.zone"+v);
                        });
                    }
                    apiHost.stats("analytics",'sensor="'+sensor._id+'" and '+settings.zonemap_query()+" and ("+fields.join("=* or ")+"=*)",fields,sensor._source.office).then(function (data) {
                        $.each(data,function (k,v) {
                            data[k]=v.count?v.avg:0;
                        });

                        if (sensor._source.algorithm=="crowd-counting") {
                            var rgb2hex=function (color) {
                                var hex=Number(color).toString(16);
                                return hex.length<2?"0"+hex:hex;
                            };
                            sensorctx.zonemap.eachLayer(function (layer1) {
                                var zonex="count.zone"+layer1.feature.properties.zone;
                                var color=Math.floor(Math.min(255,Math.max(0,zonex in data?data[zonex]/1000.0*256:0)));
                                layer1.setStyle({
                                    fillColor: "#"+rgb2hex(color)+"0000",
                                    fillOpacity: 0.3,
                                    weight: 0.5,
                                });
                            });
                        }
                        stats.update(stat_layer,sensorctx,map.getZoom(),sensor,data,iconloc);
                    }).catch(function () {
                        if (sensor._source.algorithm=="crowd-counting") {
                            sensorctx.zonemap.eachLayer(function (layer1) {
                                layer1.resetStyle();
                            });
                        }
                        stats.update(stat_layer,sensorctx,map.getZoom(),sensor,{},iconloc);
                    });
                }
            };
            sensorctx.close_sensor=function () {
                stats.close(sensorctx);
            };

            var add_zones=function () {
                var features=[]
                $.each(sensor._source.zones,function (x,v) {
                    features.push(officectx.zonedata[v]);
                });
                if (typeof(sensorctx.zonemap)!=="undefined")
                    sensorctx.zonemap.addData(features);
            };
            if (typeof(officectx.zonedata)==="undefined") {
                $.getJSON("images/stadium/zonemap-"+sensor._source.office.lat+"d"+sensor._source.office.lon+".json").then(function (data) {
                    var zonedata={};
                    $.each(data,function (x,v) {
                        zonedata[v.properties.zone]=v;
                    });
                    officectx.zonedata=zonedata;
                    add_zones();
                });
            } else {
                add_zones();
            }
        },
    },
};

