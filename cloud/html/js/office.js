$("#office").on("open.zf.reveal", function(e) {
    var page=$(this);
    var ctx=page.data("ctx");
    var ctx2={};

    page.find("h3").empty().append(ctx.address+" @ ["+ctx.office.lat+","+ctx.office.lon+"]");
    workload.create(ctx2,page.find('canvas'),ctx.address+" Workload");
    var update=function () {
        /* fill the algorithm table */
        apiHost.search("algorithms","name:*",ctx.office).then(function (data) {
            var tbody=page.find("[algorithm-table] tbody");
            tbody.empty();
            $.each(data.response,function (i,v) {
                var sensor=("sensor" in v._source)?'<a href="javascript:void(0)">'+v._source.sensor+"</a>":"N/A";
                var latency=("latency" in v._source)?v._source.latency.toFixed(2)+" ms":"N/A";
                var performance=("performance" in v._source)?v._source.performance.toFixed(2)+" fps":"N/A";
                var line=$("<tr><td>"+v._source.name+"</td><td>"+v._id+"</td><td>"+sensor+"</td><td>"+v._source.status+"</td><td>"+latency+"</td><td>"+performance+"</td><td>"+v._source.skip+" frame(s)</td></tr>");
                tbody.append(line);
                line.find("a").click(function () {
                    page.foundation("close");
                    selectPage("recording",['sensor="'+v._source.sensor+'"',ctx.office]);
                });
            });
        }).catch(function (e) {
        });

        /* fill the service table */
        apiHost.search("services","name:*",ctx.office).then(function (data) {
            var tbody=page.find("[service-table] tbody");
            tbody.empty();
            $.each(data.response,function (i,v) {
                var line=$("<tr><td>"+v._source.name+"</td><td>"+v._source.service+"</td><td>"+v._id+"</td><td>"+v._source.status+"</td></tr>");
                tbody.append(line);
            });
        }).catch(function (e) {
        });

        /* update workloads */
        workload.update(ctx2,ctx.office);
    };

    page.data('timer', setInterval(update,2000));
}).on("closed.zf.reveal",function(e) {
    var timer=$(this).data('timer');
    if (timer) clearInterval(timer);
});
