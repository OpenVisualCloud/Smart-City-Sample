
var stats={
    create: function (ctx) {
	    ctx.circle=L.circleMarker(ctx.marker.getLatLng(), {radius:20,color:"green"});
	    ctx.text=L.tooltip({permanent:true,direction:'center',className:'tooltip_text'});
        var canvas=$('<div style="width:350px;height:150px"><canvas style="width:100%;height:100%"></canvas></div>').find("canvas");

        ctx.chart=new Chart(canvas, {
            type: 'bar',
            data: {
                labels: [],
                datasets: [],
            },
            options: {
                responsive: true,
                maintainAspectRatio: false,
                title: { display: false },
                tooltips: {
                    mode: 'index',
                    intersect: false,
                },
                scales: {
                    yAxes: [{ 
                        display: true, 
                        scaleLabel: { 
                            display: false 
                        },
                        ticks: {
                           maxTicksLimit: 5,
                        },
                        stacked: true,
                    }], 
                    xAxes: [{
                        display: true,
                        barThickness: 'flex',
                        scaleLabel: {
                            display: false,
                        },
                        type: 'time',
                        time: {
                            displayFormats: {
                                second: 'hh:mm:ss',
                            },
                        },
                        ticks: {
                            maxRotation: 0,
                            minRotation: 0,
                        },
                        stacked: true,
                    }],
                },
            },
        });
        ctx.circle.bindPopup(canvas.parent()[0],{ maxWidth:"auto",maxHeight:"auto" });
    },
    update: function (layer, ctx, zoom, sensor_id, sensor_location) {
        var update_chart=function (data) {
            var labels=ctx.chart.config.data.labels;
            var time=new Date();
            labels.push(time);

            var datasets=ctx.chart.config.data.datasets;
            $.each(datasets, function (k,v) {
                if (!(v.label in data)) return;
                v.data.push({t:time,y:data[v.label]});
                delete data[v.label];
            });
            $.each(data, function (k,v) {
                 datasets.push({label:k,data:[{t:time,y:v}]});
            });

            if (labels.length>25) {
                labels.shift();
                for (var k=datasets.length-1;k>=0;k--) {
                    while (datasets[k].data.length>0) {
                        if (datasets[k].data[0].t>=labels[0]) break;
                        datasets[k].data.shift();
                    }
                    if (datasets[k].data.length==0) 
                        datasets.splice(k,1);
                }
            }
            ctx.chart.update();
        };
        apiHost.stats("analytics",'sensor="'+sensor_id+'" and '+settings.stats_query(),settings.stats_histogram()).then(function (data) {
            var count=0;
            for (var k in data) 
                count=count+data[k];
            update_chart(data);
            if (count>0) {
                var pretty=function(value) {
                    if (value<1000) return value.toString(10);
                    for (var unit of ['K','M','B']) {
                        value=value/1000;
                        if (value<1000) 
                            return ((value<10)?value.toFixed(1):Math.floor(value))+unit;
                    }
                    return ((value<10)?value.toFixed(1):Math.floor(value))+'B';
                };
                ctx.circle.setLatLng([sensor_location.lat+0.003*Math.pow(2,14-zoom),sensor_location.lon]).addTo(layer);
                ctx.text.setLatLng(ctx.circle.getLatLng()).setContent(pretty(count)).addTo(layer);
            } else {
                ctx.circle.remove();
                ctx.text.remove();
            }
        }).catch(function () {
            ctx.circle.remove();
            ctx.text.remove();
            update_chart(0);
        });
    },
    close: function (ctx) {
        ctx.circle.remove();
        ctx.text.remove();
    },
};
