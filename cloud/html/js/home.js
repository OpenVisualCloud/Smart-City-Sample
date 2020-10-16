
function format_sensor_tooltip(template, sensor) {
    $.each(template.find("[field]"),function (x,v) {
        var value=text.translate(sensor._source[$(v).attr("field")]);
        if (typeof(value)=="string") value=value.replace(/:\/\/[^:]*:[^@]*@/,'://');
        $(v).text(text.translate(value));
    });
    template.find("[location]").text("["+sensor._source.location.lat.toFixed(3)+","+sensor._source.location.lon.toFixed(3)+"]");
    template.find("[resolution]").text(sensor._source.resolution.width+"x"+sensor._source.resolution.height);
    return template.html();
}

function marker_update_icon(marker, icon) {
    if (icon!=marker.getIcon())
        marker.setIcon(icon);
}

function sensor_line_color(officectx, sensor) {
    if (!officectx.online) return "red";
    return (sensor._source.status=="idle")?"black":(sensor._source.status=="streaming")?"green":"red";
}

function set_office_status(officectx, online) {
    var online2=officectx.online;
    officectx.online=online;
    marker_update_icon(officectx.marker, online?officectx.scenario.icon.office.online:officectx.scenario.icon.office.offline);
    if (online!=online2) 
        alerts.append(new Date,officectx.address,online?text["office online"]:text["office offline"],online?"info":"fatal");
}

$("#pg-home").on(":initpage", function(e) {
    var page=$(this);
    $("#layoutButton").hide();

    /* create map */
    var map=page.data('map');
    if (!map) {
        page.data('zoom', 15);
        page.data('offices',{});
        page.data('sensors',{});
        page.data('queries',"type=*");

        /* create map */
        map=L.map("mapCanvas",{ zoom: page.data('zoom'), minZoom: 13 });
        page.data('map',map);

        /* add layers switching widget */
        page.data('lineinfo',{ name: text["connection info"], layer: L.layerGroup() });
        page.data('heatmap',{ name: text["density estimation"], layer: L.layerGroup() });
        page.data('stat',{ name: text["statistics histogram"], layer: L.layerGroup() });
        page.data('preview', { name: text["preview clips"], layer: L.layerGroup() });
        page.data('alert', { name: text["Scrolling Alerts"], layer: L.layerGroup() });
        page.data('controls', L.control.layers().addTo(map));
        alerts.setup(page);

        /* add tiles */
        $.each(scenarios.setting, function (i,sc) {
            scenarios[sc].setup(i,page,map);
        });

        map.on('zoomend', function () {
            var update_layer=function (layer) {
                var z=layer._zoomargs;
                if (!z) return;
                var scale=Math.pow(2.0,map.getZoom()-z.zoom);
                var width=Math.floor(z.width*scale);
                var height=Math.floor(z.height*scale);
                $(layer._icon).css({width:width+'px',height:height+'px'});
            };
            page.data('stat').layer.eachLayer(update_layer);
            page.data('preview').layer.eachLayer(update_layer);
        });
    }

    /* enable the office button */
    var search=$("#homeSearch");
    $("#homeButton").unbind('click').click(function () {
        map.flyTo(page.data('scenario').center, page.data('zoom'));
    });

    /* update map with the sensor info */
    var index="sensors";
    var update=function (queries) {
        if (!page.is(":visible")) return;
        page.data('queries',queries);
 
        /* remove any old timer */
        var timer=page.data('timer');
        if (timer) clearTimeout(timer);

        var center=map.getCenter();
        var offices=page.data('offices');
        var sensors=page.data('sensors');
        var scenario=page.data('scenario');
        apiHost.search("offices","location:["+center.lat+","+center.lng+","+settings.radius()+"]",null).then(function (office_reply) {
            if ("status" in office_reply) 
                $("[hint-panel]").trigger(":error",[office_reply.status]);

            $.each(office_reply.response, function (x, office_data) {
                var officeid=office_data._source.location.lat+","+office_data._source.location.lon;
                if (!(officeid in offices)) {
                    offices[officeid]={
                        office: office_data._source.location,
                        address: office_data._source.address,
                        scenario: scenario,
                        online: true,
                    };
                    var officectx=offices[officeid];

                    officectx.marker=L.marker(officectx.office, {
                        icon: scenario.icon.office.online,
                        riseOnHover: true,
                    }).addTo(map);

                    officectx.marker.bindTooltip(officectx.address+' @ ['+officeid+']').on('click', function () {
                        $("#office").data("ctx",officectx);
                        $("#office").foundation('open');
                    });
                }

                /* setup office address & tooltip */
                var officectx=offices[officeid];
                officectx.used=true;

                alerts.update(officectx, offices, sensors);
                apiHost.search(index,"("+queries+") and location:["+center.lat+","+center.lng+","+settings.radius()+"]",officectx.office).then(function (sensor_reply) {

                    if ("status" in sensor_reply) 
                        $("[hint-panel]").trigger(":error",[sensor_reply.status]);

                    set_office_status(officectx,true);
                    $.each(sensor_reply.response, function (x,sensor) {
                        var sensorid=sensor._source.location.lat+","+sensor._source.location.lon;
                        if (!(sensorid in sensors)) {
                            sensors[sensorid]={ 
                                scenario: scenario,
                                address: sensor._source.address,
                            };
                            var sensorctx=sensors[sensorid];
                            sensorctx.marker=L.marker(sensor._source.location,{
                                icon: scenario.icon.sensor_icon(sensor, officectx.online),
                                riseOnHover: true,
                                rotationAngle: scenario.icon.sensor_icon_rotation(sensor),
                                rotationOrigin: "center",
                            }).on('dblclick', function() {
                                selectPage("recording",['sensor="'+sensor._id+'"',sensor._source.office]);
                            }).on('popupopen', function () {
                                sensorctx.marker.unbindTooltip();
                            }).on('popupclose', function () {
                                sensorctx.marker.bindTooltip(sensorctx.tooltip);
                            }).addTo(map);

                            preview.create(sensorctx, sensor, page, map);
                            if (scenario.create_sensor) 
                                scenario.create_sensor(officectx, sensorctx, sensor, page, map);
        
                            sensorctx.line_dash="15,20";
                            var line_color=sensor_line_color(officectx, sensor);
                            sensorctx.line=L.polyline([sensor._source.location,sensor._source.office],{color:line_color,dashArray:sensorctx.line_dash}).bindTooltip("",{ permanent:true, direction:'center', opacity:0.7, className:'tooltip_text' }).addTo(page.data('lineinfo').layer);
                        }

                        /* update sensor */
                        var sensorctx=sensors[sensorid];
                        sensorctx.used=true;

                        /* update sensor icon */
                        marker_update_icon(sensorctx.marker, sensorctx.scenario.icon.sensor_icon(sensor, officectx.online));

                        /* update sensor info */
                        if (sensorctx.update_sensor) 
                            sensorctx.update_sensor(sensor);

                        /* update sensor tooltip */
                        var tooltip=format_sensor_tooltip($("[template] [sensor-info-template]").clone(),sensor);
                        if (sensorctx.tooltip!=tooltip) {
                            sensorctx.tooltip=tooltip;
                            sensorctx.marker.unbindTooltip().bindTooltip(tooltip);
                        }

                        /* show line info */
                        sensorctx.line.setTooltipContent(format_bandwidth("bandwidth" in sensor._source && sensor._source.status == "streaming"?sensor._source.bandwidth:0));
                        var line_color=sensor_line_color(officectx, sensor);
                        if (line_color=="green") {
                            var tmp=sensorctx.line_dash.split(",");
                            sensorctx.line_dash=tmp[1]+","+tmp[0];
                        }
                        sensorctx.line.setStyle({ color: line_color, dashArray: sensorctx.line_dash }).redraw();
                    });
                }).catch(function (e) {
                    var online=e.status<500 || e.status>504;
                    set_office_status(officectx, online);
                });
            });
        }).catch(function (e) {
            alerts.append(new Date,text["central office"],text["connection error"],"fatal");
        });

        /* remove obsolete markers */
        $.each(sensors, function (x,v) {
            if ("used" in v) {
                delete v.used;
            } else {
                if (v.close_sensor) v.close_sensor();
                if (v.marker) v.marker.remove();
                if (v.line) v.line.remove();
                preview.close(v, page);
                delete sensors[x];
            }
        });
        $.each(offices, function (x,v) {
            if ("used" in v) {
                delete v.used;
            } else {
                if (v.close_office) v.close_office();
                v.marker.remove();
                delete offices[x];
            }
        });
        page.data('timer',setTimeout(update,settings.sensor_update(),queries));
    };

    /* enable sensor queries */
    search.val(page.data("queries")).data('index',index).data('office',null).data('invoke',update).focus().trigger($.Event("keydown",{keyCode:13}));

}).on(":closepage",function() {
    var page=$(this);
    var timer=page.data('timer');
    if (timer) clearTimeout(timer);
});
