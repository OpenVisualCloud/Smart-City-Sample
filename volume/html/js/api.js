
var apiHost={
    search: function (index, queries, office, size) {
        if (typeof size=="undefined") size=25;
        var url="api/search";
        var args={index:index,queries:queries,size:size,office:office?office.lat+","+office.lon:"*"};
        console.log("GET "+url+"?"+$.param(args));
        return $.get(url,args);
    },
    stats: function (index, queries, aggs, office) {
        var url="api/stats";
        var args={ index:index, queries:queries, aggs:aggs, office:office.lat+","+office.lon};
        console.log("GET "+url+"?"+$.param(args));
        return $.get(url,args);
    },
    workload: function (office) {
        var url="api/workload";
        var args={ office:office.lat+","+office.lon }
        console.log("GET "+url+"?"+$.param(args));
        return $.get(url,args);
    },
    hint: function (index, office) {
        var url="api/hint";
        var args={ index:index, office:office?office.lat+","+office.lon:"*" };
        console.log("GET "+url+"?"+$.param(args));
        return $.get(url,args);
    },
};
