
var previews={
    add: function (map) {
        var panel=$("#preview-panel").show();
        var video=panel.find("video");
        var update=function () {
            if (!panel.is(":visible")) return;
            var center=map.getCenter();
            apiHost.search("recordings",settings.preview_query()+" and office:["+center.lat+","+center.lng+","+settings.radius()+"]",null,1).then(function (r) {
                r=r.response;
                if (r.length==0) return setTimeout(update,5000);
                video.find("source").attr('src','recording/'+r[0]._source.path+'?'+$.param({office:r[0]._source.office.lat+","+r[0]._source.office.lon}));
                video[0].load();
                panel.find("[caption]").html("<div>Sensor: "+r[0]._source.sensor+"<br>"+"Time: "+(new Date(r[0]._source.time)).toLocaleString()+"</div>");
                panel.find("a").unbind('click').click(function () {
                    selectPage("recording",['sensor="'+r[0]._source.sensor+'"',r[0]._source.office]);
                });
            }).catch(function () {
                setTimeout(update,5000);
            });
        };
        video.unbind('ended').bind('ended',update).unbind('error').bind('error',function () {
            setTimeout(update,5000);
        });
        update();
    },
    remove: function () {
        $("#preview-panel").hide();
    },
    play: function () {
        $("#preview-panel video").get(0).play();
    },
}
