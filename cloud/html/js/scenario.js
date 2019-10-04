
var scenarios={
    traffic: {
        name: "traffic",
        center: [45.536664,-122.960823],
        icon: {
            office: L.icon({
                iconUrl: "images/office.gif",
                iconSize: [64,64],
                iconAnchor: [32,32],
            }),
            ip_camera: L.icon({
                iconUrl: "images/camera.gif",
                iconSize: [32,32],
                iconAnchor: [16,16],
            }),
        },
        setup: function (order, tiles, page, map) {
            var layer1=L.tileLayer("images/traffic/{z}/{x}/{y}.png",{
                attribution: 'Map data &copy; <a href="https://www.openstreetmap.org/">OpenStreetMap</a> contributors, <a href="https://creativecommons.org/licenses/by-sa/2.0/">CC-BY-SA</a>',
                id: 'base'
            }).on('add', function () {
                page.data('scenario', scenarios.traffic);
                map.setView(scenarios.traffic.center,page.data('zoom'));
            });
            if (order==0) layer1.addTo(map).fire('add');
            tiles["Traffic Planning"]=layer1;
        },
    },
    stadium: {
        name: "stadium",
        center: [37.388085,-121.963472],
        icon: {
            office: L.icon({
                iconUrl: "images/office.gif",
                iconSize: [64,64],
                iconAnchor: [32,32],
            }),
            ip_camera: {
                left: L.icon({
                    iconUrl: "images/queue-l.gif",
                    iconSize: [90, 32],
                    iconAnchor: [45, 16],
                }),
                right: L.icon({
                    iconUrl: "images/queue-r.gif",
                    iconSize: [90, 32],
                    iconAnchor: [45, 16],
                }),
            },    
        },
        setup: function (order, tiles, page, map) {
            var layer1=L.tileLayer('images/stadium/{z}/{x}/{y}.png',{
                tms:true
            }).on('add',function() {
                page.data('scenario', scenarios.stadium);
                map.setView(scenarios.stadium.center,page.data('zoom'));
            });
            if (!Object.keys(tiles).length) layer1.addTo(map).fire('add');
            tiles["Stadium Services"]=layer1;
        },
    },
    parking: {
        name: "parking",
        center: [33.310955,-111.932443],
        icon: {
            office: L.icon({
                iconUrl: "images/office.gif",
                iconSize: [64,64],
                iconAnchor: [32,32],
            }),
            ip_camera: L.icon({
                iconUrl: "images/camera.gif",
                iconSize: [32,32],
                iconAnchor: [16,16],
            }),
        },
        setup: function (order, tiles, page, map) {
            var layer1=L.tileLayer('images/parking/{z}/{x}/{y}.png',{
                tms:true
            }).on('add',function() {
                page.data('scenario', scenarios.parking);
                map.setView(scenarios.parking.center,page.data('zoom'));
            });
            if (!Object.keys(tiles).length) layer1.addTo(map).fire('add');
            tiles["Parking Management"]=layer1;
        },
    },
};

