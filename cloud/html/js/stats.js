
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
                        scaleLabel: {
                            display: false,
                        },
                        type: 'time',
                        time: {
                            displayFormats: {
                                second: 'mm:ss',
                            },
                        },
                        ticks: {
                            maxRotation: 0,
                            minRotation: 0,
                        },
                        stacked: true,
                    }],
                },
                plugins: {
                    colorschemes: {
                        scheme: 'tableau.Tableau10'
                    },
                },
            },
        });
    },
    create: function (sensorctx, sensor, page, map, create_chart_icon) {
	    sensorctx.text=L.tooltip({permanent:true,direction:'center',className:'tooltip_text'});
        var offset={x:0,y:0};
        var div=$('<div class="page-stats" draggable="true"><canvas class="max-size"></canvas></div>').on('dragstart', function (e) {
            if (sensorctx.chart_icon) sensorctx.chart_icon.closePopup();

            var divoffset=$(this).offset();
            offset={x:e.pageX-divoffset.left,y:e.pageY-divoffset.top};
            e.originalEvent.dataTransfer.setData('application/json',JSON.stringify(sensor));
            page.find("#mapCanvas").unbind('dragover').on('dragover', function (e) {
                e.preventDefault();
            }).unbind('drop').on('drop', function (e) {
                e.preventDefault();
                var div1=div.clone().removeAttr('draggable').css({width:'100%',height:'100%'});
                var icon1=L.divIcon({html:div1[0],iconSize:[350,200],iconAnchor:[0,0]});
                var e1={clientX:e.clientX-offset.x,clientY:e.clientY-offset.y};
                var marker1=L.marker(map.mouseEventToLatLng(e1),{icon:icon1,draggable:true}).addTo(page.data('stat').layer);
                marker1._sensor=JSON.parse(e.originalEvent.dataTransfer.getData('application/json'));
                marker1._chart=stats.create_chart(div1.find('canvas'));
                marker1._zoomargs={zoom:map.getZoom(),width:350,height:200};
                $(marker1._icon).css({'border-radius':'10px'});

                div1.append('<a class="leaflet-popup-close-button front" href="javascript:void(0)">x</a>');
                div1.find('a').click(function() {
                    page.data('stat').layer.removeLayer(marker1);
                });
            });
        });
        sensorctx.chart=stats.create_chart(div.find("canvas"));
        sensorctx.chart_icon=create_chart_icon(div[0]);
        if (!sensorctx.chart_icon) {
            sensorctx.chart_icon=L.marker(sensorctx.marker.getLatLng(), {
                icon: L.icon({
                    iconUrl: 'images/chart.png',
                    iconSize: [55,40],
                    iconAnchor: [29,15],
                }),
                opacity: 0.6,
            }).bindPopup(div[0], { maxWidth:"auto",maxHeight:"auto" });
        }
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
            datasets.push({label:k,barThickness:'flex',data:[{t:time,y:v}]});
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
    update: function (layer, sensorctx, zoom, sensor, data1, loc) {
        var count=0, data={};
        for (var k in data1) {
            count=count+data1[k];
            data[text.translate(k)]=data1[k];
        }
        stats.update_chart(sensorctx.chart, data);
        layer.eachLayer(function (layer1) {
            if (!layer1._sensor || !layer1._chart) return;
            if (layer1._sensor._id!=sensor._id || layer1._sensor._source.office.lat!=sensor._source.office.lat || layer1._sensor._source.office.lon!=sensor._source.office.lon) return;
            stats.update_chart(layer1._chart,data);
        });
        if (count>0) {
            var pretty=function(value) {
                if (value<1000) return (Math.floor(value)).toString(10);
                for (var unit of ['K','M','B']) {
                    value=value/1000;
                    if (value<1000) 
                        return ((value<10)?value.toFixed(1):Math.floor(value))+unit;
                }
                return ((value<10)?value.toFixed(1):Math.floor(value))+'B';
            };

            var iconloc=[sensor._source.location.lat+0.003*Math.pow(2,14-zoom),sensor._source.location.lon];
            if (typeof(sensorctx.chart_icon.setLatLng) !== "undefined")
                sensorctx.chart_icon.setLatLng(iconloc);
	        if(!layer.hasLayer(sensorctx.chart_icon)) 
                sensorctx.chart_icon.addTo(layer);

            sensorctx.text.setLatLng(loc?loc:iconloc).setContent(pretty(count));
	        if(!layer.hasLayer(sensorctx.text)) 
                sensorctx.text.addTo(layer);
        } else {
            if (layer.hasLayer(sensorctx.chart_icon))
                layer.removeLayer(sensorctx.chart_icon);
            sensorctx.text.setContent("");
            if (layer.hasLayer(sensorctx.text))
                layer.removeLayer(sensorctx.text);
        }
    },
    close: function (sensorctx) {
        sensorctx.chart_icon.remove();
        sensorctx.text.remove();
    },
};
