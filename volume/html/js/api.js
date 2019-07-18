
var apiHost={
    search: function (index, queries, size) {
        if (typeof size=="undefined") size=25;
        var url="api/search";
        var args={ index: index, queries: queries, size:size };
        console.log("GET "+url);
        return $.get(url,args);
    },
    stats: function (index, queries, aggs) {
        var url="api/stats";
        var args={ index: index, queries: queries, aggs: aggs };
        console.log("GET "+url);
        return $.get(url,args);
    },
    workload: function (ondata) {
        var worker=new Worker('js/worker.js');
        worker.onmessage=ondata;
        worker.postMessage(window.location.protocol.replace("http","ws")+window.location.host+window.location.pathname+"api/workload");
        return worker;
    },
    hint: function (index) {
        var url="api/hint";
        var args={ index: index };
        console.log("GET "+url);
        return $.get(url,args);
    },
};
