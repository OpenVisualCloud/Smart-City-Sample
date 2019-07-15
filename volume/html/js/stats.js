
var stats={
    pretty: function(value) {
        if (value<1000) return value.toString(10);
        for (var unit of ['K','M','B']) {
            value=value/1000;
            if (value<1000) return ((value<10)?value.toFixed(1):Math.floor(value))+unit;
        }
        return ((value<10)?value.toFixed(1):Math.floor(value))+'B';
    },
    create: function (ctx) {
	    ctx.circle=L.circleMarker(ctx.marker.getLatLng(), {radius:20,color:"green"});
	    ctx.text=L.tooltip({permanent:true,direction:'center',className:'tooltip_text'});
        var canvas=$('<div style="width:350px;height:150px"><canvas style="width:100%;height:100%"></canvas></div>').find("canvas");

        ctx.chart=new Chart(canvas, {
            type: 'bar',
            data: {
                labels: [],
                datasets: [{
                    label: "statistics",
                    data: [],
                }],
            },
            options: {
                responsive: true,
                maintainAspectRatio: false,
                title: { display: false },
                legend: { display: false },
                scales: {
                    yAxes: [{ 
                        display: true, 
                        scaleLabel: { 
                            display: false 
                        },
                        ticks: {
                           maxTicksLimit: 5,
                        },
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
                    }],
                },
            },
        });
        ctx.circle.bindPopup(canvas.parent()[0],{ maxWidth:"auto",maxHeight:"auto" });
    },
    update: function (layer, ctx, zoom, sensor_id, sensor_location) {
        var update_chart=function (count) {
            var labels=ctx.chart.config.data.labels;
            var time=new Date();
            labels.push(time);

            var datasets=ctx.chart.config.data.datasets;
            datasets[0].data.push({t:time,y:count});

            if (labels.length>25) {
                labels.shift();
                datasets[0].data.shift();
            }
            ctx.chart.update();
        };
        apiHost.count("analytics",'sensor="'+sensor_id+'" and '+settings.stats_query()).then(function (count) {
            count=parseInt(count,10);
            update_chart(count);
            if (count>0) {
                ctx.circle.setLatLng([sensor_location.lat+0.003*Math.pow(2,14-zoom),sensor_location.lon]).addTo(layer);
                ctx.text.setLatLng(ctx.circle.getLatLng()).setContent(stats.pretty(count)).addTo(layer);
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
