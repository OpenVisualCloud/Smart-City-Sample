
var previews={
    create: function (page, ctx, sensor, map, layer) {
        var div=page.find("[preview-template]").clone();
        div.removeAttr("preview-template").show();
        ctx.marker.bindPopup(div[0],{
            maxWidth:"auto",
            maxHeight:"auto",
        }).on('click',function () {
            if ("video" in ctx) {
                ctx.video.remove();
                delete ctx.video;
            }
            ctx.marker.closeTooltip();
            previews.play(div,sensor);

            div.attr('draggable','true').bind('dragstart',function (e) {
                e.originalEvent.dataTransfer.setData("application/json",JSON.stringify(sensor));
                page.find("#mapCanvas").unbind('dragover').on('dragover', function (e) {
                    e.preventDefault();
                }).unbind('drop').on('drop', function (e) {
                    e.preventDefault();
                    var div=page.find("[preview-template]").clone().show();
                    div.removeAttr("preview-template").css({width:'100%',height:'100%'});
                    var icon=L.divIcon({html:div[0],iconSize:[300,200],iconAnchor:[0,0]});
                    var marker=L.marker(map.mouseEventToLatLng(e),{icon:icon,draggable:true}).addTo(layer);
                    marker._zoomargs={zoom:map.getZoom(),width:300,height:200};
                    $(marker._icon).css({'border-radius':'10px'});
                    var sensor1=JSON.parse(e.originalEvent.dataTransfer.getData("application/json"));
                    previews.play(div,sensor1);

                    div.append('<a class="leaflet-popup-close-button" href="javascript:void(0)" style="z-index:100">x</a>').find('a').click(function() {
                        marker.remove();
                    });
                });
            });
        });
    },
    play: function (div, sensor) {
        var update=function () {
            var error='<div style="line-height:200px;text-align:center">Recording Unavailable</div>';
            apiHost.search("recordings","time>=now-200000 and sensor='"+sensor._id+"'",sensor._source.office,1).then(function (r) {
                div.find("div,video").remove();
                r=r.response;
                if (r.length==0) {
                    div.append(error);
                    return setTimeout(update,5000);
                }
                var video=$('<video style="width:100%;height:100%" autoplay muted><source src="recording/'+r[0]._source.path+'?'+$.param({office:sensor._source.office.lat+","+sensor._source.office.lon})+'"></source></video>').bind('ended',update).bind('error',function () {
                    setTimeout(update,5000);
                });
                div.append(video);
            }).catch(function () {
                div.find("div,video").remove();
                div.append(error);
                setTimeout(update,5000);
            });
        };
        update();
    },
};
