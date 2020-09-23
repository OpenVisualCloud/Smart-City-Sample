
function api_host_url (office, url) {
    if (!office) return "cloud/"+url;
    var t=(office.lat+"c"+office.lon).replace(/\./g,'d').replace(/-/g,'n');
    return "offices/"+t+"/"+url;
}

var apiHost={
    search: function (index, queries, office, size) {
        if (typeof size=="undefined") size=25;
        var url=api_host_url(office,"api/search");
        var args={index:index,queries:queries,size:size};
        console.log("GET "+url+"?"+$.param(args));
        return $.get(url,args);
    },
    histogram: function (index, queries, field, size, office) {
        var url=api_host_url(office,"api/histogram");
        var args={index:index,queries:queries,field:field,size:size};
        console.log("GET "+url+"?"+$.param(args));
        return $.get(url,args);
    },
    stats: function (index, queries, fields, office) {
        var url=api_host_url(office,"api/stats");
        var args={index:index,queries:queries,fields:fields.join(",")};
        console.log("GET "+url+"?"+$.param(args));
        return $.get(url,args);
    },
    workload: function (office) {
        var url=api_host_url(office,"api/workload");
        var args={}
        console.log("GET "+url+"?"+$.param(args));
        return $.get(url,args);
    },
    hint: function (index, office) {
        var url=api_host_url(office,"api/hint");
        var args={ index:index };
        console.log("GET "+url+"?"+$.param(args));
        return $.get(url,args);
    },
};
