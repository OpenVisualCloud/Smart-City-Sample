
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
    workload: function (ondata, office) {
        var worker=new Worker('js/worker.js');
        worker.onmessage=ondata;
        worker.postMessage(window.location.protocol.replace("http","ws")+window.location.host+window.location.pathname+"api/workload?"+$.param({office:office.lat+","+office.lon}));
        return worker;
    },
    hint: function (index, office) {
        var url="api/hint";
        var args={ index:index, office:office?office.lat+","+office.lon:"*" };
        console.log("GET "+url+"?"+$.param(args));
        return $.get(url,args);
    },
};
