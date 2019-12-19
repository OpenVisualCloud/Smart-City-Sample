
var workload={
    create: function (ctx, canvas, title) {
        ctx.workload=new Chart(canvas, {
            type: 'line',
            data: {
                labels: [],
                datasets: [{ 
                    label: "cpu",
                    data: [], 
                    fill: false,
                },{
                    label: "mem",
                    data: [],
                    fill: false,
                },{
                    label: "disk",
                    data: [],
                    fill: false,
                }],
            },
            options: {
                reponsive: true,
                maintainAspectRatio: false,
                title: {
                    display: true,
                    text: title,
                    padding: 0,
                    lineHeight: 1.0,
                },
                scales: {
                    yAxes: [{
                        display: true,
                        scaleLabel: {
                            display: false
                        },
                        ticks: {
                            min: 0,
                            max: 100,
                        },
                    }],
                    xAxes: [{
                        display: true,
                        scaleLabel: {
                            display: false
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
                plugins: {
                    colorschemes: {
                        scheme: 'tableau.Tableau20'
                    },
                },
            }
        });
        ctx.workload_update=new Date();
    },
    update: function (ctx, office) {
        if ((new Date()-ctx.workload_update)<2000) return;
        ctx.workload_update=new Date();

        apiHost.workload(office).then(function (data) {
            var labels=ctx.workload.config.data.labels;
            var time=new Date(data.time);
            labels.push(time);

            var datasets=ctx.workload.config.data.datasets;
            datasets[0].data.push({t:time,y:data.cpu.toFixed(0)});
            datasets[1].data.push({t:time,y:((data.memory[0]-data.memory[1])/data.memory[0]*100).toFixed(0)});
            datasets[2].data.push({t:time,y:data.disk[3].toFixed(0)});

            if (labels.length>20) {
                labels.shift();
                datasets[0].data.shift();
                datasets[1].data.shift();
                datasets[2].data.shift();
            }
            ctx.workload.update();
        });
    },
    close: function (ctx) {
    },
}; 
