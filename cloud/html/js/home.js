$("#pg-home").on(":initpage", function(e) {
    var page=$(this);
    $("#layoutButton").hide();
    $("#cloudButton").hide();

    /* create map */
    var map=page.data('map');
    if (!map) {
        page.data('zoom', 15);
        page.data('sensors',{});
        page.data('offices',{});
        page.data('queries',"sensor=*");

        /* create map */
        map=L.map("mapCanvas",{ zoom: page.data('zoom'), minZoom: 13 });
        page.data('map',map);

        /* add tiles */
        var tiles={};
        $.each(scenarios.setting, function (i,sc) {
            scenarios[sc].setup(i,tiles,page,map);
        });

        /* add layers switching widget */
        var heatmap_layer=L.layerGroup().addTo(map);
        page.data('heatmaps',heatmap_layer);
        var stats_layer=L.layerGroup().addTo(map);
        page.data('stats',stats_layer);
        var preview_layer=L.layerGroup().addTo(map);
        page.data('previews',preview_layer);
        var alert_layer=L.layerGroup().addTo(map);
        page.data('alerts',alert_layer);
        alerts.setup(page, alert_layer);

        L.control.layers(tiles,{
            "Density Estimation": heatmap_layer,
            "Statistics Histogram": stats_layer,
            "Preview Clips": preview_layer, 
            "Scrolling Alerts": alert_layer,
        }).addTo(map);

        map.on('zoomend', function () {
            var update_layer=function (layer) {
                var z=layer._zoomargs;
                if (!z) return;
                var scale=Math.pow(2.0,map.getZoom()-z.zoom);
                var width=Math.floor(z.width*scale);
                var height=Math.floor(z.height*scale);
                $(layer._icon).css({width:width+'px',height:height+'px'});
            };
            stats_layer.eachLayer(update_layer);
            preview_layer.eachLayer(update_layer);
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
            var sensors=page.data('sensors');
            var offices=page.data('offices');
            var stats_layer=page.data('stats');
            var heatmap_layer=page.data('heatmaps');
            var preview_layer=page.data('previews');
            var scenario=page.data('scenario');

            $.each(data.response, function (x,info) {
                var tmp=[];
                $.each([
                    ["Type",info._source.sensor],
                    ["Model",info._source.model],
                    ["Address", info._source.address],
                    ["Location","["+info._source.location.lat.toFixed(3)+","+info._source.location.lon.toFixed(3)+"]"],
                    ["Office","["+info._source.office.lat.toFixed(3)+","+info._source.office.lon.toFixed(3)+"]"],
                    ["MAC",info._source.mac],
                    ["Resolution",info._source.resolution.width+"x"+info._source.resolution.height],
                    ["URL",info._source.url],
                    ["Theta",info._source.theta],
                    ["Mnt-H",info._source.mnth],
                    ["Alpha",info._source.alpha],
                    ["FOV-H",info._source.fovh],
                    ["FOV-V",info._source.fovv],
                    ["Status", info._source.status],
                ],function (x,v) {
                    tmp.push("<tr><td>"+v[0]+"</td><td>"+v[1]+"</td></tr>");
                });
                var title='<table style="border-collapse:collapse;line-height:0.5rem"><tbody>'+tmp.join("")+"</tbody></table>";

                var officeid=info._source.office.lat+","+info._source.office.lon;
                if (officeid in offices) {
                    offices[officeid].used=true;
                } else {
                    offices[officeid]={
                        office: info._source.office,
                        marker: L.marker(info._source.office, { 
                            icon: scenario.icon.office,
                            riseOnHover: true,
                        }).addTo(map),
                        used: true,
                    };
                }

                /* setup office address & tooltip */
                if (!("address" in offices[officeid])) {
                    apiHost.search('offices','location:['+officeid+']',null,1).then(function (data) {
                        if (data.response.length==0) return;
                        var ctx=offices[officeid];
                        ctx.address=data.response[0]._source.address;

                        /* setup marker actions */
                        ctx.marker.bindTooltip(ctx.address+' @ ['+officeid+']').on('click', function () {
                            $("#office").data("ctx",ctx);
                            $("#office").foundation('open');
                        });
                    }).catch(function () {
                    });
                }

                var sensorid=info._source.location.lat+","+info._source.location.lon;
                var line_color=(info._source.status=="idle")?"black":(info._source.status=="streaming")?"green":"red";
                if (sensorid in sensors) {
                    var ctx=sensors[sensorid];
                    ctx.used=true;
                    if (line_color=="green") {
                        var tmp=ctx.line_dash.split(",");
                        ctx.line_dash=tmp[1]+","+tmp[0];
                    }
                    ctx.line.setStyle({ color: line_color, dashArray: ctx.line_dash }).redraw();
                } else {
                    sensors[sensorid]={ 
                        address: info._source.address,
                        marker: L.marker(info._source.location,{
                            icon: scenario.icon[info._source.model],
                            riseOnHover:true,
                            rotationAngle:"theta" in info._source?360+90-info._source.theta:0,
                            rotationOrigin:"center",
                        }).on('dblclick',function() {
                            selectPage("recording",['sensor="'+info._id+'"',info._source.office]);
                        }).addTo(map),
                        line: L.polyline([info._source.location,info._source.office],{color:line_color,dashArray:"15,20"}).addTo(map).bindTooltip("",{ permanent:true, direction:'center', opacity:0.7, className:'tooltip_text' }),
                        line_dash: "15,20",
                        used: true,
                    };

                    var ctx=sensors[sensorid];
                    previews.create(page, ctx, info, map, preview_layer);
		            stats.create(ctx, info, page, map, stats_layer);
                    heatmaps.create(ctx,info._source.location);

                    /* disable tooltip while popup open */
                    ctx.marker.on('popupopen',function () {
                        ctx.marker.unbindTooltip();
                    }).on('popupclose',function () {
                        ctx.marker.bindTooltip(ctx.title);
                    });
                }

                /* show bandwidth */
                var bandwidth=("bandwidth" in info._source && info._source.status == "streaming")?info._source.bandwidth:0, unit="b/s";
                if (bandwidth>1024) { bandwidth=bandwidth/1024; unit="Kb/s"; }
                if (bandwidth>1024) { bandwidth=bandwidth/1024; unit="Mb/s"; }
                if (bandwidth>1024) { bandwidth=bandwidth/1024; unit="Gb/s"; }
                sensors[sensorid].line.setTooltipContent(bandwidth>0?bandwidth.toFixed(1)+unit:"");

                /* show bubble stats */
                if (map.hasLayer(stats_layer)) 
                    stats.update(stats_layer, sensors[sensorid], map.getZoom(), info);

                /* show heatmaps */
                if (map.hasLayer(heatmap_layer)) 
                    heatmaps.update(heatmap_layer, sensors[sensorid], map.getZoom(), info);

                /* show workload */
                var popup=offices[officeid].marker.getPopup();
                if (popup && popup.isOpen())
                    workloads.update(offices[officeid],info._source.office);

                if (sensors[sensorid].title!=title) {
                    sensors[sensorid].marker.unbindTooltip().bindTooltip(title);
                    sensors[sensorid].title=title;
                }
            });

            /* remove obsolete markers */
            $.each(sensors, function (x,v) {
                if ("used" in v) {
                    delete v.used;
                } else {
                    if ("video" in v) v.video.remove();
                    v.marker.remove();
                    v.line.remove();
		            stats.close(v);
                    heatmaps.close(v);
                    workloads.close(v);
                    delete sensors[x];
                }
            });
            $.each(offices, function (x,v) {
                if ("used" in v) {
                    delete v.used;
                } else {
                    map.removeLayer(v.marker);
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
