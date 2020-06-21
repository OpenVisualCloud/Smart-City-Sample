
var preview={
    create: function (sensorctx, sensor, page, map) {
        var div=$("[template] [preview-template]").clone().dblclick(function () {
            selectPage("recording",['sensor="'+sensor._id+'"',sensor._source.office]);
        }).addClass("page-home-preview-screen-size");

        sensorctx.marker.bindPopup(div[0],{
            maxWidth:"auto",
            maxHeight:"auto",
        }).on('click',function () {
            sensorctx.marker.closeTooltip();
            preview.play(div,sensor);

            var offset={x:0,y:0};
            div.attr('draggable','true').bind('dragstart',function (e) {
                sensorctx.marker.closePopup();

                var divoffset=$(this).offset();
                offset={x:e.pageX-divoffset.left,y:e.pageY-divoffset.top};
                e.originalEvent.dataTransfer.setData("application/json",JSON.stringify(sensor));
                page.find("#mapCanvas").unbind('dragover').on('dragover', function (e) {
                    e.preventDefault();
                }).unbind('drop').on('drop', function (e) {
                    e.preventDefault();
                    preview.close(sensorctx, page);

                    var div=$("[template] [preview-template]").clone().addClass("max-size");
                    var icon=L.divIcon({html:div[0],iconSize:[300,200],iconAnchor:[0,0]});
                    var e1={clientX:e.clientX-offset.x,clientY:e.clientY-offset.y};
                    var marker=L.marker(map.mouseEventToLatLng(e1),{icon:icon,draggable:true}).addTo(page.data('preview').layer);
                    marker._zoomargs={zoom:map.getZoom(),width:300,height:200};
                    $(marker._icon).addClass("page-home-preview-screen");
                    sensorctx.video=marker;

                    var sensor1=JSON.parse(e.originalEvent.dataTransfer.getData("application/json"));
                    marker.on('add', function (e) {
                        preview.play(div,sensor1);
                    }).on('remove', function (e) {
                        div.find("div,video").remove();
                    }).fire('add');

                    div.append('<a class="leaflet-popup-close-button front" href="javascript:void(0)">x</a>').find('a').click(function() {
                        preview.close(sensorctx, page);
                    });
                });
            });
        });
    },
    play: function (div, sensor) {
        var update=function () {
            var error='<div class="page-home-preview-screen-recording-unavailable">'+text["recording-unavailable"]+'</div>';
            apiHost.search("recordings",settings.preview_query()+" and sensor='"+sensor._id+"'",sensor._source.office,1).then(function (r) {
                div.find("div,video").remove();
                r=r.response;
                if (r.length==0) {
                    div.append(error);
                    return setTimeout(update,5000);
                }
                var video=$('<video class="max-size" autoplay muted><source src="recording/'+r[0]._source.path+'?'+$.param({office:sensor._source.office.lat+","+sensor._source.office.lon})+'"></source></video>').bind('ended',update).bind('error',function () {
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
    close: function (sensorctx, page) {
        if ("video" in sensorctx) {
            page.data('preview').layer.removeLayer(sensorctx.video);
            delete sensorctx.video;
        }
    },
};
