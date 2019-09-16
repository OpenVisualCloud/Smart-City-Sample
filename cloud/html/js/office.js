$("#pg-office").on(":initpage", function(e, queries, office) {
    var page=$(this);
    $("#layoutButton").hide();
    $("#cloudButton").hide();

    /* update home button */
    $("#homeButton").unbind('click').click(function () {
        selectPage('home');
    });

    var search=$("#homeSearch");
    var index="algorithms";
    var updateAlgos=function (queries) {
        if (!page.is(":visible")) return;
        page.data('queries',queries);

        /* remove old timer */
        var timer=page.data('timer');
        if (timer) clearTimeout(timer);
        
        /* fill the algorithm table */
        apiHost.search(index,queries,office).then(function (data) {
            var tbody=page.find("[algorithm-table] tbody");
            tbody.empty();
            $.each(data.response,function (i,v) {
                var sensor=("sensor" in v._source)?v._source.sensor:"N/A";
                var latency=("latency" in v._source)?v._source.latency.toFixed(2)+" ms":"N/A";
                var performance=("performance" in v._source)?v._source.performance.toFixed(2)+" fps":"N/A";
                var line=$("<tr><td>"+v._source.name+"</td><td>"+v._id+"</td><td>"+sensor+"</td><td>"+v._source.status+"</td><td>"+latency+"</td><td>"+performance+"</td><td>"+v._source.skip+" frame(s)</td></tr>");
                tbody.append(line);
                line.find("a").click(function () {
                    selectPage("recording",['sensor="'+v._source.source+'"',office]);
                });
            });

            page.data('timer',setTimeout(updateAlgos,settings.analytics_update(),queries));
        }).catch(function (e) {
            $("[hint-panel]").trigger(":error", [e.statusText]);
        });

    };

    /* setup the service table */
    var updateService=function () {
        if (!page.is(":visible")) return;

        /* fill the service table */
        apiHost.search("services","name:*",office).then(function (data) {
            var tbody=page.find("[service-table] tbody");
            tbody.empty();
            $.each(data.response,function (i,v) {
                var line=$("<tr><td>"+v._source.name+"</td><td>"+v._source.service+"</td><td>"+v._id+"</td><td>"+v._source.status+"</td></tr>");
                tbody.append(line);
            });

            if (page.data('timer2')) clearTimeout(page.data('timer2'));
            page.data('timer2',setTimeout(updateService,settings.service_update()));
        }).catch(function (e) {
            $("[hint-panel]").trigger(":error", [e.statusText]);
        });
    }; 
    updateService();

    /* enable recording queries */
    search.data('index',index).data('office',office).data('invoke',updateAlgos).val(queries).focus().trigger($.Event("keydown",{keyCode:13}));

    /* enable workload charts */
    var ctx={};
    workloads.create(ctx,page.find('canvas'),"Server Workload");
    ctx.timer=setInterval(workloads.update,2000,ctx,office);
    page.data('workload',ctx);
}).on(":closepage",function() {
    var page=$(this);

    var timer=page.data('timer');
    if (timer) clearTimeout(timer);

    var ctx=page.data('workload');
    if (ctx) clearInterval(ctx.timer);
});
