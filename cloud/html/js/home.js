
function format_sensor_tooltip(template, sensor) {
    $.each(template.find("td[field]"),function (x,v) {
        $(v).text(sensor._source[$(v).attr("field")]);
    });
    template.find("[location]").text("["+sensor._source.location.lat.toFixed(3)+","+sensor._source.location.lon.toFixed(3)+"]");
    template.find("[resolution]").text(sensor._source.resolution.width+"x"+sensor._source.resolution.height);
    return template.html();
}

$("#pg-home").on(":initpage", function(e) {
    var page=$(this);
    $("#layoutButton").hide();
    $("#cloudButton").hide();

    /* create map */
    var map=page.data('map');
    if (!map) {
        page.data('zoom', 15);
        page.data('offices',{});
        page.data('sensors',{});
        page.data('queries',"sensor=*");

        /* create map */
        map=L.map("mapCanvas",{ zoom: page.data('zoom'), minZoom: 13 });
        page.data('map',map);

        /* add layers switching widget */
        page.data('lineinfo',{ name: "Connection Info", layer: L.layerGroup() });
        page.data('heatmap',{ name: "Density Estimation", layer: L.layerGroup() });
        page.data('stat',{ name: "Statistics Histogram", layer: L.layerGroup() });
        page.data('preview', { name: "Preview Clips", layer: L.layerGroup() });
        page.data('alert', { name: "Scrolling Alerts", layer: L.layerGroup() });
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
        map.setView(page.data('scenario').center, page.data('zoom'));
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
        apiHost.search(index,"("+queries+") and location:["+center.lat+","+center.lng+","+settings.radius()+"]",null).then(function (data) {
            var offices=page.data('offices');
            var sensors=page.data('sensors');
            var scenario=page.data('scenario');

            $.each(data.response, function (x,sensor) {
                var officeid=sensor._source.office.lat+","+sensor._source.office.lon;
                if (!(officeid in offices)) {
                    offices[officeid]={
                        office: sensor._source.office,
                        marker: L.marker(sensor._source.office, { 
                            icon: scenario.icon.office,
                            riseOnHover: true,
                        }).addTo(map),
                    };
                }

                /* setup office address & tooltip */
                var officectx=offices[officeid];
                officectx.used=true;
                if (!("address" in officectx)) {
                    apiHost.search('offices','location:['+officeid+']',null,1).then(function (data) {
                        if (data.response.length==0) return;
                        officectx.address=data.response[0]._source.address;

                        /* setup marker actions */
                        officectx.marker.bindTooltip(officectx.address+' @ ['+officeid+']').on('click', function () {
                            $("#office").data("ctx",officectx);
                            $("#office").foundation('open');
                        });
                    }).catch(function () {
                    });
                }

                var sensorid=sensor._source.location.lat+","+sensor._source.location.lon;
                if (!(sensorid in sensors)) {
                    sensors[sensorid]={ 
                        scenario: scenario,
                        address: sensor._source.address,
                    };
                    var sensorctx=sensors[sensorid];
                    sensorctx.marker=L.marker(sensor._source.location,{
                        icon: scenario.icon.sensor_icon(sensor),
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
                    var line_color=(sensor._source.status=="idle")?"black":(sensor._source.status=="streaming")?"green":"red";
                    sensorctx.line=L.polyline([sensor._source.location,sensor._source.office],{color:line_color,dashArray:sensorctx.line_dash}).bindTooltip("",{ permanent:true, direction:'center', opacity:0.7, className:'tooltip_text' }).addTo(page.data('lineinfo').layer);
                }

                /* update sensor */
                var sensorctx=sensors[sensorid];
                sensorctx.used=true;

                /* update sensor icon */
                var icon=sensorctx.scenario.icon.sensor_icon(sensor);
                if (icon!=sensorctx.marker.getIcon())
                    sensorctx.marker.setIcon(icon);

                /* update sensor info */
                if (sensorctx.update_sensor) 
                    sensorctx.update_sensor(sensor);

                /* update sensor tooltip */
                var tooltip=format_sensor_tooltip(page.find("[sensor-info-template]").clone().removeAttr('sensor-info_template').show(),sensor);
                if (sensorctx.tooltip!=tooltip) {
                    sensorctx.tooltip=tooltip;
                    sensorctx.marker.unbindTooltip().bindTooltip(tooltip);
                }

                /* show line info */
                sensorctx.line.setTooltipContent(format_bandwidth("bandwidth" in sensor._source && sensor._source.status == "streaming"?sensor._source.bandwidth:0));
                var line_color=(sensor._source.status=="idle")?"black":(sensor._source.status=="streaming")?"green":"red";
                if (line_color=="green") {
                    var tmp=sensorctx.line_dash.split(",");
                    sensorctx.line_dash=tmp[1]+","+tmp[0];
                }
                sensorctx.line.setStyle({ color: line_color, dashArray: sensorctx.line_dash }).redraw();
            });

            /* remove obsolete markers */
            $.each(sensors, function (x,v) {
                if ("used" in v) {
                    delete v.used;
                } else {
                    if (v.close_sensor) v.close_sensor();
                    if (v.marker) v.marker.remove();
                    if (v.line) v.line.remove();
                    preview.close(v);
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
        }).catch(function (e) {
            $("[hint-panel]").trigger(":error", [e.statusText]);
            page.data('timer',setTimeout(update,settings.sensor_update(),queries));
        });
    };

    /* enable sensor queries */
    search.val(page.data("queries")).data('index',index).data('office',null).data('invoke',update).focus().trigger($.Event("keydown",{keyCode:13}));

}).on(":closepage",function() {
    var page=$(this);
    var timer=page.data('timer');
    if (timer) clearTimeout(timer);
});
