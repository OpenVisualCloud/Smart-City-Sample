
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
        return $.get(url,args);
    },
    histogram: function (index, queries, field, size, office) {
        var url=api_host_url(office,"api/histogram");
        var args={index:index,queries:queries,field:field,size:size};
        return $.get(url,args);
    },
    stats: function (index, queries, fields, office) {
        var url=api_host_url(office,"api/stats");
        var args={index:index,queries:queries,fields:fields.join(",")};
        return $.get(url,args);
    },
    workload: function (office) {
        var url=api_host_url(office,"api/workload");
        var args={}
        return $.get(url,args);
    },
    hint: function (index, office) {
        var url=api_host_url(office,"api/hint");
        var args={ index:index };
        return $.get(url,args);
    },
    sensors: function (sensor, office) {
        var url=api_host_url(office,"api/sensors");
        var args={ sensor:sensor };
        return $.post(url,args);
    },
    tokens: function (roomid, office) {
        var url=api_host_url(office,"api/tokens");
        var args={ room:roomid };
        return $.post(url,args);
    },
};
