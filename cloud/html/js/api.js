
var apiHost={
    search: function (index, queries, office, size) {
        if (typeof size=="undefined") size=25;
        var url="api/search";
        var args={index:index,queries:queries,size:size,office:typeof office=='string'?office:office.lat+","+office.lon};
        console.log("GET "+url+"?"+$.param(args));
        return $.get(url,args);
    },
    histogram: function (index, queries, field, size, office) {
        var url="api/histogram";
        var args={index:index,queries:queries,field:field,size:size,office:office.lat+","+office.lon};
        console.log("GET "+url+"?"+$.param(args));
        return $.get(url,args);
    },
    stats: function (index, queries, fields, office) {
        var url="api/stats";
        var args={index:index,queries:queries,fields:fields.join(","),office:office.lat+","+office.lon};
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
        var args={ index:index, office:typeof office=='string'?office:office.lat+","+office.lon };
        console.log("GET "+url+"?"+$.param(args));
        return $.get(url,args);
    },
    health: function (zone) {
        var url="api/health";
        var args={ zone: zone }
        console.log("GET "+url+"?"+$.param(args));
        return $.get(url,args);
    },
};
