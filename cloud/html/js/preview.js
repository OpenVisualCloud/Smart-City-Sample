
var preview={
    create: function (sensorctx, sensor, page, map) {
        var div=$("[template] [preview-template]").clone().addClass("page-home-preview-screen-size");

        var worker=null;
        sensorctx.marker.bindPopup(div[0],{
            maxWidth:"auto",
            maxHeight:"auto",
        }).on('popupopen',function () {
            sensorctx.marker.closeTooltip();

            if (worker) worker.close();
            worker=preview.play(div,sensor);

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

                    var worker1;
                    var sensor1=JSON.parse(e.originalEvent.dataTransfer.getData("application/json"));
                    marker.on('add', function (e) {
                        worker1=preview.play(div,sensor1);
                    }).on('remove', function (e) {
                        div.find("video,div").remove();
                        worker1.close();
                    }).fire('add');

                    div.append('<a class="leaflet-popup-close-button front" href="javascript:void(0)">x</a>').find('a').click(function() {
                        preview.close(sensorctx, page);
                    });
                });
            });
        }).on('popupclose', function () {
            if (worker) worker.close();
        });
    },
    play: function (div, sensor) {
        var div_show=function (message) {
            div.find("div,video").remove();
            div.append(message);
        };
        div_show('<div class="page-home-preview-screen-recording-unavailable">'+text["recording-loading"]+'</div>');

        var error='<div class="page-home-preview-screen-recording-unavailable">'+text["recording-unavailable"]+'</div>';
        var conference=new Owt.Conference.ConferenceClient();
        apiHost.sensors(sensor._id,sensor._source.office).then(function (data) {
            apiHost.tokens(data.room,sensor._source.office).then(function (token) {

                window.sessionStorage.officePath="/offices/"+(sensor._source.office.lat+"c"+sensor._source.office.lon).replace(/-/g,'n').replace(/\./g,'d');

                conference.join(token).then(function (r) {
                    var stream1=null;
                    for (var i in r.remoteStreams) {
                        var stream=r.remoteStreams[i];
                        if (data.stream==stream.id) stream1=stream;
                    }
                    if (stream1) {
                        conference.subscribe(stream1,{audio:false}).then(function (s) {
                            div_show('<video class="max-size" autoplay muted></video>');
                            div.find("video")[0].srcObject = stream1.mediaStream;
                        }, function () {
                            div_show(error);
                        });
                    } else {
                        div_show(error);
                    }
                }, function () {
                    div_show(error);
                });
            }).catch(function () {
                div_show(error);
            });
        }).catch(function () {
            div_show(error);
        });
        return { 
            close: function () { 
                conference.leave().catch(function () {});
            },
        };
    },
    close: function (sensorctx, page) {
        if ("video" in sensorctx) {
            page.data('preview').layer.removeLayer(sensorctx.video);
            delete sensorctx.video;
        }
    },
};
