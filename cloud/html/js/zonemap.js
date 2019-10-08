
var zonemap={
    setup: function (map, officectx, officeid) {
        officectx.zonemap=[];
        $.get("stadium/zonemap-"+officeid+".json",function (data) {
            $.each(data, function (k,v) {
               ctx.zonemap.push(L.geoJSON(v,{}));
            });
        }).catch(function (e) {
            console.log(e);
        });
    },
    update: function (ctx, sensor) {
        if (!ctx.zonemap) return;
        apiHost.search("analytics",'sensor="'+sensor._id+'" and '+settings.zonemap_query(),sensor._source.office,100).then(function (data) {
            var counts={};
            ctx.zonemap.eachLayer(function (layer) {
                counts[layer.properties.zone]=Math.random()*100;
            });
            $.each(data.response, function (k1,v1) {
                if (!("counts" in v1._source)) return;
                $.each(v1._source.counts, function (k2, v2) {
                    counts[v2.zone]=counts[v2.zone]+v2.count;
                });
            });
            ctx.zonemap.setStyle(function (feature) {
                var zone=feature.properties.zone;
                var style={ color: "#00ff00", opacity: 0.1, weight: 5 };
                if (counts[zone]>50) style={ color: "#ffff00", opacity: 0.5, weight: 10 };
                if (counts[zone]>80) style={ color: "#ff0000", opacity: 0.9, weight: 20 };
                return style;
            });
        }).catch(function (e) {
        });
    },
    close: function (ctx) {
        if (ctx.zonemap) ctx.zonemap.remove();
    },
};
