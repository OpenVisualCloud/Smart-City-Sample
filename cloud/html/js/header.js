
var settings={
    radius: function (val) {
        if (typeof(val)!="undefined") $("#mapRadius").val(val);
        return parseFloat($("#mapRadius").val());
    },
    sensor_update: function (val) {
        if (typeof(val)!="undefined") $("#sensorUpdate").val(val);
        return parseFloat($("#sensorUpdate").val());
    },
    service_update: function (val) {
        if (typeof(val)!="undefined") $("#serviceUpdate").val(val);
        return parseFloat($("#serviceUpdate").val());
    },
    frame_duration: function (val) {
        if (typeof(val)!="undefined") $("#frameDuration").val(val);
        return parseFloat($("#frameDuration").val());
    },
    alert_window: function (val) {
        if (typeof(val)!="undefined") $("#alertWindow").val(val);
        return parseFloat($("#alertWindow").val());
    },
    preview_query: function (val) {
        if (typeof(val)!="undefined") $("#previewQueries").val(val);
        return $("#previewQueries").val();
    },
    heatmap_query: function (val) {
        if (typeof(val)!="undefined") $("#heatmapQueries").val(val);
        return $("#heatmapQueries").val();
    },
    stats_query: function (val) {
        if (typeof(val)!="undefined") $("#statsQueries").val(val);
        return $("#statsQueries").val();
    },
    stats_histogram: function (val) {
        if (typeof(val)!="undefined") $("#statsHistogram").val(val);
        return $("#statsHistogram").val();
    },
}

$("#settingPanel button").click(function() {
    var page=$(this);
});

function showHints() {
    var page=$("#homeSearch");
    var desc=page.data('desc');
    var candidates=page.data('candidates');
    var candidateIdx=page.data('candidateIdx');

    var hintText=(desc!="")?'<div style="background-color:lightgrey;margin-bottom:5px">'+desc+"</div>":"";
    var s=(candidateIdx>9)?candidateIdx-9:0;
    var e=(s+10>=candidates.length)?candidates.length:s+10;
    for (var i=s;i<e;i++) {
        if (i==candidateIdx) {
            hintText=hintText+"<span style='background-color:lightblue'>"+candidates[i]+"</span><BR>";
        } else {
            hintText=hintText+candidates[i]+"<BR>";
        }
    }
    var panel=$("[hint-panel]");
    if (hintText!="") {
        panel.trigger(":display", [hintText]);
    } else {
        panel.hide();
    }
}

$("#homeSearch").on("focus", function () {
    var page=$(this);
    $("[hint-panel]").hide();
    apiHost.hint(page.data('index'),page.data('office')).then(function (hints) {
        page.data('hints',hints);
    });
}).keydown(function (e) {
    var page=$(this);
    var candidates=page.data('candidates'); 
    var candidateIdx=page.data('candidateIdx'); 

    if (e.keyCode==9) {
        e.preventDefault();
        e.stopPropagation();
        if (candidates.length==0) return;
        var text=page.val().substring(0,page[0].selectionStart);
        var text2=candidates[candidateIdx];
        for (var i=text2.length;i>=0;i--) {
            if (i>=text2.length || text.substring(text.length-i)!=text2.substring(0,i)) continue;
            page.val(text+text2.substring(i));
            page.trigger('input');
            return;
        }
    } else if (e.keyCode==38) {
        e.preventDefault();
        e.stopPropagation();
        if (candidateIdx==0) return;
        page.data('candidateIdx',candidateIdx-1);
        showHints();
    } else if (e.keyCode==40) {
        e.preventDefault();
        e.stopPropagation();
        if (candidateIdx>=candidates.length-1) return;
        page.data('candidateIdx',candidateIdx+1);
        showHints();
    } else if (e.keyCode==13) {
        $("[hint-panel]").hide();
        page.data('invoke')(page.val());
    }
}).on("input",function (e) {
    var page=$(this);

    var textPrep=function (text) {
        return text.replace(/"[^"]*"*/,'""').replace(/'[^']*'*/,"''").replace(/ ([Aa][Nn][Dd]|[Oo][Rr]|[Nn][Oo][Tt]|[Ww][Hh][Ee][Rr][Ee]) /g,'&&');
    };
    var textHelp=function (hints, ltext, rtext, text) {
        var candidates=[""];
        ltext=ltext.split(/[\&\|\!\(\)\]\+\-\*\/]/).pop().replace(/\s/g,"");
        $.each(hints, function (w, wc) {
            if (!wc.values || wc.values.length==0) {
                if (w.startsWith(ltext)) candidates.push(w);
            }
            $.each(wc.values, function (x, value) {
                var query=w+'="'+value+'"';
                if (query.startsWith(ltext)) candidates.push(query);
            });
            if (w!=text) return;
            if (wc["type"]=="date") {
                candidates[0]="Search date time: VAR>MM/DD/YYYY, VAR<hh/mm/ss[.uuu], or VAR>=MM/DD/YYYY hh/mm/ss[.uuu], where hh is in 24 hours.";
            }
            if (wc["type"] in {"long":1,"float":1,"integer":1,"short":1,"byte":1,"double":1}) {
                var range="";
                if ("min" in wc) range=" ["+wc.min+"-)";
                if ("max" in wc) if ("min" in wc) range=" ["+wc.min+"-"+wc.max+"]"; else range=" (-"+wc.max+"]";
                candidates[0]="Search numbers"+range+": VAR=&lt;expr&gt; or VAR&gt;=&lt;expr&gt;";
            }
            if (wc["type"]=="text") {
                candidates[0]='Search strings: VAR:"string" or VAR="string"';
            }
            if (wc["type"]=="geo_point") {
                candidates[0]="Search geometric locations: VAR:[&lt;lat&gt;,&lt;lon&gt;] or VAR:[&lt;lat&gt;,&lt;lon&gt;,&lt;radius&gt;].";
            }
        });
        return candidates;
    };

    var text=page.val(), cursor=page.get(0).selectionStart;
    var rtext=textPrep(text.substring(cursor));
    var ltext=text.substring(0,cursor);
    var indexes=page.data('index').split(',');
    var index=indexes[(indexes.length>1 && ltext.match(/ [Ww][Hh][Ee][Rr][Ee] /))?1:0];
    ltext=textPrep(ltext);
    var varp=/[a-z_A-Z0-9.<=>:\[, ]/i, s, e;
    for (s=ltext.length-1;s>=0&&varp.test(ltext.charAt(s));s--) {}
    for (e=0;e<rtext.length&&varp.test(rtext.charAt(e));e++) {}
    text=(ltext.substring(s+1)+rtext.substring(0,e)).split(/[<=>:]/)[0].replace(/\s/g,"");

    var candidates=textHelp(page.data('hints')[index], ltext, rtext, text);
    var desc=candidates.shift();
    var candidateIdx;
    for (candidateIdx=0;candidateIdx<candidates.length;candidateIdx++)
        if (candidates[candidateIdx].startsWith(page.val())) break;
    if (candidateIdx>=candidates.length) candidateIdx=0;

    page.data('candidates',candidates);
    page.data('candidateIdx',candidateIdx);
    page.data('desc',desc);
    showHints();
});

$("[hint-panel]").on(":display", function (e, message) {
    var panel=$(this);
    var page=$("#homeSearch");

    panel.html('<div>'+message+'</div>');
    var height=panel.find("div:first")[0].scrollHeight;
    if (height<32) height=32;
    panel.css({
        top:(3+page.offset().top+page.outerHeight())+"px",
        left:page.offset().left+"px",
        width:page.outerWidth()+"px",
        height:height+"px"
    });
    panel.show();
}).on(":error", function (e, message) {
    $(this).trigger(":display", ['<p style="color:red">'+message+'</p>']);
});

$(window).resize(function () {
    $("#ContentWindow").css({height:"calc(100vh - "+$(".top-bar").outerHeight()+"px)"});
});
