var alerts={
    setup: function (page, layer) {
        layer.on('add', function () {
            $("[alert-screen]").show();
        }).on('remove', function () {
            $("[alert-screen]").hide();
        });
        setTimeout(alerts.update,5000);

        $("[alert-screen]").bind('dragstart',function (e) {
            var screen=$(this);
            var rect=screen[0].getBoundingClientRect();
            var offsetX=e.clientX-rect.left;
            var offsetY=e.clientY-rect.top;

            page.find("#mapCanvas").unbind('dragover').on('dragover', function (e) {
                e.preventDefault();
            }).unbind('drop').on('drop', function (e) {
                e.preventDefault();
                screen.css({left:e.clientX-offsetX+'px',top:e.clientY-offsetY+'px'});
            });
        });
    },
    append: function (time,office,text,level) {
        var screen=$("[alert-screen] ul");
        var timestamp=time.toLocaleDateString(undefined,{
            dateStyle:'short',timeStyle:'short', hour12:false,
        });
        var colors={info:"#4AFC0B",warning:"#F7FA0C",fatal:"#FF0013"};
        var li=$('<li style="color:'+colors[level]+';font-size:0">'+timestamp+' @['+office.lat+','+office.lon+']: '+text+'</li>');
        li.data('time',time);

        var exist=false;
        $.each(screen.find("li"),function (x,l1) {
            if (li.text()==$(l1).text()) exist=true;
        });
        if (!exist) {
            screen.prepend(li);
            screen.find("li:first").animate({'font-size':'1em'});
        }

        if (screen.find("li").length>50)
            screen.find("li:last").remove();
    },
    update: function () {
        var screen=$("[alert-screen]");
        if (screen.is(":visible")) {
            apiHost.search("alerts","time>=now-"+settings.alert_window(),null).then(function (r) {
                $.each(r.response, function (x,r1) {
                    var time=new Date(r1._source.time);
                    $.each(["info","warning","fatal"], function (x, level) {
                        if (!(level in r1._source)) return;
                        $.each(r1._source[level], function (x,v) {
                            alerts.append(time,r1._source.office,v.message,level);
                        });
                    });
                });
            }).catch(function () {
            });
        }
        setTimeout(alerts.update,5000);
    },
};

