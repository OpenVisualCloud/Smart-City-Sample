
var origAfterFit = Chart.Legend.prototype.afterFit;
Chart.Legend.prototype.afterFit = function () {
    origAfterFit.call(this);
    if (this.options && this.options.maxHeight) {
        this.height = Math.min(this.height, this.options.maxHeight);
        this.minSize.height = Math.min(this.minSize.height, this.height);
    }
};

var stats={
    create_chart: function (canvas) {
        return new Chart(canvas, {
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
                legend: {
                    position: 'top',
                    labels: {
                        fontSize: 9,
                    },
                    display: true,
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
    },
    create: function (ctx, sensor, page, map, layer) {
	    ctx.circle=L.circleMarker(ctx.marker.getLatLng(), {radius:20,color:"green"});
	    ctx.text=L.tooltip({permanent:true,direction:'center',className:'tooltip_text'});
        var div=$('<div style="width:350px;height:200px;padding-top:5px;padding-bottom:5px" draggable="true"><canvas style="width:100%;height:100%"></canvas></div>').on('dragstart', function (e) {
            e.originalEvent.dataTransfer.setData('application/json',JSON.stringify(sensor));
            page.find("#mapCanvas").unbind('dragover').on('dragover', function (e) {
                e.preventDefault();
            }).unbind('drop').on('drop', function (e) {
                e.preventDefault();
                var div1=div.clone().removeAttr('draggable').css({width:'100%',height:'100%'});
                var icon1=L.divIcon({html:div1[0],iconSize:[350,200],iconAnchor:[0,0]});
                var marker1=L.marker(map.mouseEventToLatLng(e),{icon:icon1,draggable:true}).addTo(layer);
                marker1._sensor=JSON.parse(e.originalEvent.dataTransfer.getData('application/json'));
                marker1._chart=stats.create_chart(div1.find('canvas'));
                marker1._zoomargs={zoom:map.getZoom(),width:350,height:200};

                div1.append('<a class="leaflet-popup-close-button" href="javascript:void(0)" style="z-index:100">x</a>');
                div1.find('a').click(function() {
                    marker1.remove();
                });
            });
        });
        ctx.chart=stats.create_chart(div.find("canvas"));
        ctx.circle.bindPopup(div[0],{ maxWidth:"auto",maxHeight:"auto" });
    },
    update_chart: function (chart, data) {
        var labels=chart.config.data.labels;
        var time=new Date();
        labels.push(time);

        data=Object.assign({},data);
        var datasets=chart.config.data.datasets;
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
        chart.config.options.legend.display=(datasets.length<4);
        chart.update();
    },
    update: function (layer, ctx, zoom, sensor) {
        apiHost.stats("analytics",'sensor="'+sensor._id+'" and '+settings.stats_query(),settings.stats_histogram(),25,sensor._source.office).then(function (data) {
            var count=0;
            for (var k in data) 
                count=count+data[k];
            stats.update_chart(ctx.chart, data);
            layer.eachLayer(function (layer1) {
                if (!layer1._sensor || !layer1._chart) return;
                if (layer1._sensor._id!=sensor._id || layer1._sensor._source.office.lat!=sensor._source.office.lat || layer1._sensor._source.office.lon!=sensor._source.office.lon) return;
                stats.update_chart(layer1._chart,data);
            });
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
                ctx.circle.setLatLng([sensor._source.location.lat+0.003*Math.pow(2,14-zoom),sensor._source.location.lon]).addTo(layer);
                ctx.text.setLatLng(ctx.circle.getLatLng()).setContent(pretty(count)).addTo(layer);
            } else {
                ctx.circle.remove();
                ctx.text.remove();
            }
        }).catch(function () {
            ctx.circle.remove();
            ctx.text.remove();
            stats.update_chart(ctx.chart, {});
        });
    },
    close: function (ctx) {
        ctx.circle.remove();
        ctx.text.remove();
    },
};
