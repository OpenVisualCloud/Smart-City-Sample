
var previews={
    create: function (page, ctx, sensor, layer) {
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
            });
        });
    },
    play: function (div, sensor) {
        var update=function () {
            var error='<div style="line-height:200px;text-align:center">No Recording(s)</div>';
            apiHost.search("recordings","time>=now-200000 and sensor='"+sensor._id+"'",sensor._source.office,1).then(function (r) {
                r=r.response;
                if (r.length==0) {
                    div.empty().append(error);
                    return setTimeout(update,5000);
                }
                var title=$('<div style="position:absolute;width:100%;top:0;text-align:center;font-size:1em">['+sensor._source.location.lat+","+sensor._source.location.lon+"]</div>");
                var video=$('<video style="position:absolute;top:0;width:100%;height:100%" autoplay muted><source src="recording/'+r[0]._source.path+'?'+$.param({office:sensor._source.office.lat+","+sensor._source.office.lon})+'"></source></video>').bind('ended',update).bind('error',function () {
                    setTimeout(update,5000);
                });
                div.empty().append(title).append(video);
            }).catch(function () {
                div.empty().append(error);
                setTimeout(update,5000);
            });
        };
        update();
    },
    dropSetup: function (canvas, map, layer) {
        canvas.on('dragover', function (e) {
            e.preventDefault();
        }).on('drop', function (e) {
            e.preventDefault();
            var sensor=JSON.parse(e.originalEvent.dataTransfer.getData("application/json"));
            var div=canvas.parent().find("[preview-template]").clone();
            div.removeAttr("preview-template").show();
            var icon=L.divIcon({html:div[0],iconSize:[300,200],shadowSize:[300,200]});
            var marker=L.marker(map.mouseEventToLatLng(e),{icon:icon,draggable:true}).addTo(layer);
            previews.play(div,sensor);
        });
    },
};
