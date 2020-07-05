$("#pg-recording").on(":initpage", function(e, queries, office) {
    var page=$(this);

    /* setup the layout button */
    $("#layoutButton").show().unbind('click').click(function () {
        $(this).find("i").toggleClass("fi-zoom-out").toggleClass("fi-zoom-in");
        page.find("[layout1]").toggle();
        page.find("[layout4]").toggle();
    });

    /* update home button */   
    $("#homeButton").unbind('click').click(function () {
        selectPage('home');
    });

    /* enable recording queries */
    var monitor=0;
    $("#homeSearch").data('index','recordings').data('office',office).data('invoke',function (queries) {
        var plist=page.find("[play-list]");
        plist.empty();
        apiHost.search($("#homeSearch").data('index'),queries,office).then(function (data) {
            data.response.sort(function(a,b){return a._source.time-b._source.time});
            $.each(data.response, function (k,v) {
                var time=new Date(v._source.time).toLocaleString();
                v._source.office=office;
                v._source.path=v._source.path+"?"+(office?$.param({office:office.lat+","+office.lon}):'');
                var address=("address" in v._source)?v._source.address:"";
                var line=$('<tr><td class="no-padding"><a href="javascript:void(0)"><img src="thumbnail/'+v._source.path.replace(".mp4",".mp4.png")+'&size=640:360" draggable="true"/><figcaption class="xx-small">'+address+' '+time+'</figcaption></a></td></tr>');
                line.find("img").css({width:plist.width()+"px"});
                line.on("dragstart",function (e) {
                    e.originalEvent.dataTransfer.setData("application/json",JSON.stringify(v));
                });
                line.find("a").click(function () {
                    var videos=page.find("video:visible");
                    var e=$.Event('drop',{originalEvent:{dataTransfer:{getData:function(){
                        return JSON.stringify(v);
                    }}}});
                    e.preventDefault=function () {};
                    $(videos[monitor%videos.length]).trigger(e);
                    monitor=monitor+1;
                });
                plist.append(line);
            });
        }).catch(function (e) {
            $("[hint-panel]").trigger(":error", [decodeURIComponent(e.statusText)]);
        });
    });

    /* reset video screens */
    $.each(page.find("video"),function (x,v) { 
        v.pause();
        $(v).parent().find("div").empty();
    });
    $("#homeSearch").val(queries).focus().trigger($.Event("keydown",{keyCode:13}));
}).on(":closepage",function() {
});

$(window).resize(function () {
    var page=$("#pg-recording");
    page.find("[play-list]").css({height:(page.height()-2)+"px"});
    var vw4=Math.floor(page.width()*2/5);
    var vh4=Math.floor(page.height()/2);
    page.find("[layout4] video").css({width:(vw4-4)+"px","max-width":(vw4-4)+"px",height:(vh4-4)+"px","max-height":(vh4-4)+"px"}).parent().css({width:vw4+"px",height:vh4+"px"});
    var vw1=Math.floor(page.width()*4/5);
    var vh1=page.height();
    page.find("[layout1] video,svg").css({width:(vw1-2)+"px","max-width":(vw1-2)+"px",height:(vh1-2)+"px","max-height":(vh1-2)+"px"}).parent().css({width:(vw1-2)+"px",height:(vh1-2)+"px"});
});

$("#pg-recording [layout4] video").on("drop",function (e) {
    e.preventDefault();
    var page=$(this);
    var doc=JSON.parse(e.originalEvent.dataTransfer.getData("application/json"));
    page.find("source").prop('src','recording/'+doc._source.path);
    page.get(0).load();
    page.parent().find("div").text(new Date(doc._source.time).toLocaleString());
}).on("dragover",function (e) {
    e.preventDefault();
});

$("#pg-recording [layout1] video").on("drop",function (e) {
    e.preventDefault();
    var page=$(this);
    var doc=JSON.parse(e.originalEvent.dataTransfer.getData('application/json'));

    apiHost.search("sensors","_id='"+doc._source.sensor+"'",doc._source.office,1).then(function (data) {
        page.parent().find("div").text(data.response[0]._source.address+" "+new Date(doc._source.time).toLocaleString());
    });
    page.find("source").prop('src','recording/'+doc._source.path);
    draw_analytics(page, doc);
}).on("dragover",function (e) {
    e.preventDefault();
});

$("#cloudButton").click(function () {
    selectPage("recording",['sensor=*',""]);
}).on(":initwatcher", function () {
    var button=$(this);
    var timer=setInterval(function () {
        apiHost.search("recordings","sensor=*","",1).then(function (data) {
            if (data.response.length==0) return;
            clearInterval(timer);
            button.show();
        });
    }, 5000);
}).hide();
