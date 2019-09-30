
var alerts={
    setup: function (layer) {
        layer.on('add', function () {
            $("[alert-screen]").show();
        }).on('remove', function () {
            $("[alert-screen]").hide();
        });
        setTimeout(alerts.update,5000);
    },
    append: function (time,office,text,level) {
        var screen=$("[alert-screen]");
        var timestamp=time.toLocaleDateString(undefined,{
            dateStyle:'short',timeStyle:'short', hour12:false,
        });
        var colors={info:"#145A32",warning:"#7D6608",fatal:"#641E16"};
        var p=$('<p style="color:'+colors[level]+'">'+timestamp+' @['+office.lat+','+office.lon+']: '+text+'</p>');
        p.data('time',time);

        var exist=false;
        $.each(screen.find("p"),function (x,p1) {
            if (p.text()==$(p1).text()) exist=true;
        });
        if (!exist) screen.append(p);

        while (screen.find("p").length>9)
            screen.find("p:first").remove();
    },
    update: function () {
        var page=$("[alert-screen]");
        if (page.is(":visible")) {
            apiHost.search("alerts","time>=now-"+settings.alert_window(),null).then(function (r) {
                $.each(r.response, function (x,r1) {
                    var time=new Date(r1._source.time);
                    $.each(r1._source, function (k,v) {
                        if (k.endsWith("_required") && "text" in v)
                            alerts.append(time,r1._source.office,v.text,v.level);
                    });
                });
            }).catch(function () {
            });
        }
        setTimeout(alerts.update,5000);
    },
};

