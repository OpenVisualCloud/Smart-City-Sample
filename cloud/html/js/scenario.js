
function update_control_options(page, map, options) {
    var control=page.data('controls');
    $.each(options, function (layer_name,layer_choice) {
        var layer_object=page.data(layer_name);
        control.removeLayer(layer_object.layer);
        if (layer_choice) {
            control.addOverlay(layer_object.layer, layer_object.name);
            if (!map.hasLayer(layer_object.layer)) layer_object.layer.addTo(map);
        } else {
            if (map.hasLayer(layer_object.layer)) layer_object.layer.remove();
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
                    'zonemap': false,
                });
            });
            if (order==0) layer1.addTo(map).fire('add');
            page.data('controls').addBaseLayer(layer1,"Traffic Planning");
        },
        create_sensor: function (sensorctx, sensor, map) {
            sensorctx.marker=L.marker(sensor._source.location,{
                icon: scenarios.traffic.icon[sensor._source.model],
                riseOnHover:true,
                rotationAngle:90-sensor._source.theta,
                rotationOrigin:"center",
            }).on('dblclick',function() {
                selectPage("recording",['sensor="'+sensor._id+'"',sensor._source.office]);
            }).on('popupopen',function () {
                sensorctx.marker.unbindTooltip();
            }).on('popupclose',function () {
                sensorctx.marker.bindTooltip(sensorctx.title);
            }).addTo(map),
            sensorctx.line_dash="15,20";
            var line_color=(sensor._source.status=="idle")?"black":(sensor._source.status=="streaming")?"green":"red";
            sensorctx.line=L.polyline([sensor._source.location,sensor._source.office],{color:line_color,dashArray:sensorctx.line_dash}).bindTooltip("",{ permanent:true, direction:'center', opacity:0.7, className:'tooltip_text' }).addTo(map);
        },
        update_sensor: function (sensorctx, sensor) {
            /* show bandwidth */
            sensorctx.line.setTooltipContent(format_bandwidth("bandwidth" in sensor._source && sensor._source.status == "streaming"?sensor._source.bandwidth:0));

            /* alter line style */
            var line_color=(sensor._source.status=="idle")?"black":(sensor._source.status=="streaming")?"green":"red";
            if (line_color=="green") {
                var tmp=sensorctx.line_dash.split(",");
                sensorctx.line_dash=tmp[1]+","+tmp[0];
            }
            sensorctx.line.setStyle({ color: line_color, dashArray: sensorctx.line_dash }).redraw();
        },
        update_tooltip: function (sensorctx, tooltip) {
            sensorctx.marker.unbindTooltip().bindTooltip(tooltip);
        },
        close_sensor: function (sensorctx) {
            sensorctx.marker.remove();
            sensorctx.line.remove();
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
            ip_camera: {
                left: L.icon({
                    iconUrl: "images/queue-l.gif",
                    iconSize: [90, 32],
                    iconAnchor: [45, 16],
                }),
                right: L.icon({
                    iconUrl: "images/queue-r.gif",
                    iconSize: [90, 32],
                    iconAnchor: [45, 16],
                }),
            },    
        },
        setup: function (order, page, map) {
            var layer1=L.tileLayer('images/stadium/{z}/{x}/{y}.png',{
                tms:true
            }).on('add',function() {
                page.data('scenario', scenarios.stadium);
                map.setView(scenarios.stadium.center,page.data('zoom'));
                update_control_options(page, map, {
                    'heatmap': false,
                    'stat': true,
                    'preview': true,
                    'alert': true,
                    'zonemap': true,
                });
            });
            if (order==0) layer1.addTo(map).fire('add');
            page.data('controls').addBaseLayer(layer1,"Stadium Services");
        },
    },
};

