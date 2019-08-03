
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
                var video=$('<video draggable="true" style="width:100%;height:100%" autoplay muted><source src="recording/'+r[0]._source.path+'?'+$.param({office:sensor._source.office.lat+","+sensor._source.office.lon})+'"></source></video>');
                div.empty().append(video);
                video.bind('ended',update).bind('error',function () {
                    setTimeout(update,5000);
                }).bind('dragstart',function (e) {
                    e.originalEvent.dataTransfer.setData("application/json",JSON.stringify(sensor));
                });
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
            var icon=L.divIcon({html:div[0]});
            var marker=L.marker(map.mouseEventToLatLng(e),{icon:icon,draggable:true}).addTo(layer);
            previews.play(div,sensor);
        });
    },
};
