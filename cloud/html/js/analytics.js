
function draw_analytics(video, doc) {
    var colors_id=["#24693d","#44914e","#73ba67","#ced7c3","#f8816b","#e33f43","#a3123a"];
    var colors_label={ "person": "red", "vehicle": "cyan", "bike": "lime" };
    apiHost.search("analytics",'sensor="'+doc._source.sensor+'" and time>='+doc._source.time+' and time<'+(doc._source.time+doc._source.duration*1000),doc._source.office,10000).then(function (data) {
        /* group time into time buckets */
        var timed={};
        var duration=settings.frame_duration();
        var is_opera=window.navigator.userAgent.indexOf("OPR") > -1 || window.navigator.userAgent.indexOf("Opera") > -1;
        var is_edge=window.navigator.userAgent.indexOf("Edge") > -1;
        var is_chrome=!!window.chrome && !is_opera && !is_edge;
        var offset= is_chrome?0:doc._source.start_time*1000;
        $.each(data.response, function (x, v) {
            var tid=Math.floor((v._source.time-doc._source.time-offset)/duration);
            if (!(tid in timed)) timed[tid]=[];
            timed[tid].push(v);
        });

        var svg=video.parent().find('svg');
        var draw=function () {
            var tid=Math.floor((new Date()-video.data('time_offset'))/duration);
            if (tid!=video.data('last_draw')) {
                video.data('last_draw',tid);

                svg.empty();
                if (tid in timed) {
                    var sx=svg.width()/video[0].videoWidth;
                    var sy=svg.height()/video[0].videoHeight;
                    var sxy=Math.min(sx,sy);
                    var sw=sxy*video[0].videoWidth;
                    var sh=sxy*video[0].videoHeight;
                    var sxoff=(svg.width()-sw)/2;
                    var syoff=(svg.height()-sh)/2;

                    $.each(timed[tid], function (x,v) {
                        $.each(v._source.objects, function (x1, v1) {
                            if ("detection" in v1) {
                                if ("bounding_box" in v1.detection) {
                                    var xmin=v1.detection.bounding_box.x_min*sw;
                                    var xmax=v1.detection.bounding_box.x_max*sw;
                                    var ymin=v1.detection.bounding_box.y_min*sh;
                                    var ymax=v1.detection.bounding_box.y_max*sh;
                                    if (xmin!=xmax && ymin!=ymax) {
                                        svg.append($(document.createElementNS(svg.attr('xmlns'),"rect")).attr({
                                            x:sxoff+xmin,
                                            y:syoff+ymin,
                                            width:xmax-xmin,
                                            height:ymax-ymin,
                                            stroke:colors_label[v1.detection.label],
                                            "stroke-width":1,
                                            fill:"none",
                                        }));
                                        var id=("id" in v1)?":#"+v1.id+":":":";
                                        svg.append($(document.createElementNS(svg.attr('xmlns'),"text")).attr({
                                            x:sxoff+xmin,
                                            y:syoff+ymin,
                                            fill: ("id" in v1)?colors_id[v1.id%colors_id.length]:"cyan",
                                        }).text(text.translate(v1.detection.label)+id+Math.floor(v1.detection.confidence*100)+"%"));
                                    }
                                }
                            }
                        });
                    });
                }
            }
            if (video[0].paused) return video.data("time_offset",0);
            requestAnimationFrame(draw);
        };

        /* start playback */
        video[0].load();
        video.unbind('timeupdate').on('timeupdate',function () {
            var tmp=video.data('time_offset');
            video.data('time_offset',new Date()-video[0].currentTime*1000);
            if (!tmp) draw();
        }).unbind('loadedmetadata').on('loadedmetadata',function () {
            console.log("loadedmetadata="+video[0].currentTime);
        }).unbind('loadeddata').on('loadeddata',function () {
            console.log("loadeddata="+video[0].currentTime);
        });
        video.data('time_offset',new Date()-video[0].currentTime*1000);
        draw();
    }).catch(function () {
        video[0].load();
    });
}
