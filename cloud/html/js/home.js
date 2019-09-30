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
        page.data('icons',{});
        page.data('queries',"sensor=*");

        /* create map */
        map=L.map("mapCanvas",{ zoom: page.data('zoom'), minZoom: 13 });
        page.data('map',map);

        /* add tiles */
        var tiles={};
        $.each(settings.scenarios, function (i,sc) {
            if (sc=="traffic") {
                var layer1=L.tileLayer("images/street/{z}/{x}/{y}.png",{
                    attribution: 'Map data &copy; <a href="https://www.openstreetmap.org/">OpenStreetMap</a> contributors, <a href="https://creativecommons.org/licenses/by-sa/2.0/">CC-BY-SA</a>',
                    id: 'base'
                }).on('add', function () {
                    page.data('center', settings.street_center());
                    map.setView(page.data('center'),page.data('zoom'));
                });
                if (!Object.keys(tiles).length) layer1.addTo(map).fire('add');
                tiles["Traffic Planning"]=layer1;
            }
            if (sc=="parking") {
                var layer1=L.tileLayer('images/parking/{z}/{x}/{y}.png',{
                    tms:true
                }).on('add',function(){
                    page.data('center', settings.parking_center());
                    map.setView(page.data('center'),page.data('zoom'));
                });
                if (!Object.keys(tiles).length) layer1.addTo(map).fire('add');
                tiles["Parking Management"]=layer1;
            }
            if (sc=="stadium") {
                var layer1=L.tileLayer('images/stadium/{z}/{x}/{y}.png',{
                    tms:true
                }).on('add',function(){
                    page.data('center', settings.stadium_center());
                    map.setView(page.data('center'),page.data('zoom'));
                });
                if (!Object.keys(tiles).length) layer1.addTo(map).fire('add');
                tiles["Stadium Services"]=layer1;
            }
        });

        /* add layers switching widget */
        var heatmap_layer=L.layerGroup().addTo(map);
        page.data('heatmaps',heatmap_layer);
        var stats_layer=L.layerGroup().addTo(map);
        page.data('stats',stats_layer);
        var preview_layer=L.layerGroup().addTo(map);
        page.data('previews',preview_layer);
        var alert_layer=L.layerGroup();
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
        map.setView(page.data('center'), page.data('zoom'));
    });

    /* update map with the sensor info */
    var animation=[20,15];
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
            var icons=page.data('icons');

            $.each(data.response, function (x,info) {
                var tmp=[];
                $.each([
                    ["Type",info._source.sensor],
                    ["Model",info._source.model],
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

                var options={ color: 'red', dashArray: animation.join(',') };
                if (info._source.status == "idle") options.color='black';
                if (info._source.status == "streaming") options.color='green';
                animation=[animation[1],animation[0]];

                var officeid=info._source.office.lat+","+info._source.office.lon;
                if (officeid in offices) {
                    offices[officeid].used=true;
                } else {
                    var icon="images/office.gif";
                    if (!(icon in icons)) {
                        icons[icon]=L.icon({
                            iconUrl: icon,
                            iconSize: [64,64],
                            iconAnchor: [32,32],
                        });
                    }
                    
                    var ctx=offices[officeid]={
                        marker: L.marker(info._source.office, { 
                            icon: icons[icon],
                            riseOnHover: true,
                        }),
                        used: true,
                    };

                    /* setup office tooltip */
                    ctx.marker.bindTooltip("["+info._source.office.lat+","+info._source.office.lon+"]");

                    /* setup marker actions */
                    var chartdiv=$('<div style="width:300px;height:200px"><canvas style="width:100%;height:100%"></canvas></div>');
                    ctx.marker.on('dblclick', function () {
                        selectPage('office', ["name=*",info._source.office]);
                    }).bindPopup(chartdiv[0],{
                        maxWidth:"auto",
                        maxHeight:"auto"
                    }).addTo(map);

                    /* setup workload chart */
                    workloads.create(ctx,chartdiv.find("canvas"),'Office ['+officeid+']');
                }

                if (!(info._source.icon in icons)) {
                    icons[info._source.icon]=L.icon({
                        iconUrl: 'images/'+info._source.icon,
                        iconSize: [32,32],
                        iconAnchor: [16,16],
                    });
                }

                if (info._id in sensors) {
                    sensors[info._id].used=true;
                    sensors[info._id].line.setStyle(options).redraw();
                } else {
                    var marker=L.marker(info._source.location,{
                        icon: icons[info._source.icon],
                        riseOnHover:true,
                        rotationAngle:"theta" in info._source?360-info._source.theta:0,
                        rotationOrigin:"center",
                    }).addTo(map).on('dblclick',function() {
                        selectPage("recording",['sensor="'+info._id+'"',info._source.office]);
                    });

                    var ctx=sensors[info._id]={ 
                        marker: marker,
                        line: L.polyline([info._source.location,info._source.office],options).addTo(map).bindTooltip("",{ permanent:true, direction:'center', opacity:0.7, className:'tooltip_text' }),
                        used: true 
                    };
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
                sensors[info._id].line.setTooltipContent(bandwidth>0?bandwidth.toFixed(1)+unit:"");

                /* show bubble stats */
                if (map.hasLayer(stats_layer)) 
                    stats.update(stats_layer, sensors[info._id], map.getZoom(), info);

                /* show heatmaps */
                if (map.hasLayer(heatmap_layer)) 
                    heatmaps.update(heatmap_layer, sensors[info._id], map.getZoom(), info);

                /* show workload */
                if (offices[officeid].marker.getPopup().isOpen())
                    workloads.update(offices[officeid],info._source.office);

                if (sensors[info._id].title!=title) {
                    sensors[info._id].marker.unbindTooltip().bindTooltip(title);
                    sensors[info._id].title=title;
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
