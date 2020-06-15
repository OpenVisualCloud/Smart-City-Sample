var alerts={
    setup: function (page) {
        var screen=$(".page-home-alert-screen");

        page.data('alert').layer.on('add', function () {
            screen.show();
        }).on('remove', function () {
            screen.hide();
        });
        setTimeout(alerts.update,5000,page.data('map'),page.data('offices'),page.data('sensors'));

        screen.bind('dragstart',function (e) {
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
    append: function (time,address,text,level) {
        var screen=$(".page-home-alert-screen ul");
        var timestamp=time.toLocaleDateString(undefined,{
            dateStyle:'short',timeStyle:'short', hour12:false,
        });
        var colors={info:"#4AFC0B",warning:"#F7FA0C",fatal:"#FF0013"};
        var li=$('<li>'+timestamp+' @'+address+': '+text+'</li>').css({color:colors[level],"font-size":0});
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
    update: function (map, offices,sensors) {
        var screen=$(".page-home-alert-screen");
        if (screen.is(":visible")) {
            var center=map.getCenter();
            apiHost.search("alerts","time>=now-"+settings.alert_window()+" and location:["+center.lat+","+center.lng+","+settings.radius()+"]","$*").then(function (r) {
                $.each(r.response, function (x,r1) {
                    var time=new Date(r1._source.time);
                    $.each(["info","warning","fatal"], function (x, level) {
                        if (!(level in r1._source)) return;
                        $.each(r1._source[level], function (x,v) {
                            var id=r1._source.location.lat+","+r1._source.location.lon;
                            var address='['+id+']';
                            if (id in offices) address=offices[id].address;
                            if (id in sensors) address=sensors[id].address;
                            alerts.append(time,address,v.message,level);
                        });
                    });
                });
            }).catch(function () {
            });
        }
        setTimeout(alerts.update,5000,map,offices,sensors);
    },
};

