
function workloadSetup(canvas, title) {
    var chart=new Chart(canvas, {
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
            elements: {
                line: {
                    tension:0,
                }
            },
            animation: {
                duration:0,
            },
            hover: {
                animationDuration:0,
            },
            responsiveAnimationDuration:0,
        }
    });

    var worker=apiHost.workload(function (e) {
        var data=JSON.parse(e.data);
        if (data.cpu>75) $("#pg-office").trigger(":alert",["System Busy"]);
        if (!canvas.is(":visible")) return worker.terminate();

        var labels=chart.config.data.labels;
        var time=new Date(data.time);
        labels.push(time);

        var datasets=chart.config.data.datasets;
        datasets[0].data.push({t:time,y:data.cpu.toFixed(0)});
        datasets[1].data.push({t:time,y:((data.memory[0]-data.memory[1])/data.memory[0]*100).toFixed(0)});
        datasets[2].data.push({t:time,y:data.disk[3].toFixed(0)});

        if (labels.length>20) {
            labels.shift();
            datasets[0].data.shift();
            datasets[1].data.shift();
            datasets[2].data.shift();
        }
        chart.update();
    });
}

