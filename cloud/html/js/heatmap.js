
class CameraProjection {
    // # W: width of camera video frame in pixel
    // # H: height of camera video frame in pixel
    // # Hc: Height of mounted camera in meter
    // # Alpha: angle of camera optical axis relative to earth surface
    // # BetaV: vertical field of view
    // # BetaH: horizontal field of view
    // # lat: latitude of camera in degree
    // # lon: longitude of camera in degree
    // # Theta: angle of camera optical axis relative to north
    constructor(W, H, Hc, Alpha, BetaV, BetaH, lat, lon, Theta) {
        this.W = W;
        this.H = H;
        this.Hc = Hc;
        this.Alpha = Math.PI * (Alpha / 180.0);
        this.BetaH = Math.PI * (BetaH / 180.0);
        this.BetaV = 2.0 * Math.atan(Math.tan(this.BetaH / 2.0) * H / W);

        var alphaMax = 90.0 - this.BetaV / 2.0 * 180.0 / Math.PI;
        if(Alpha > alphaMax) {
            console.log('Alpha shall be smaller than ' + alphaMax + ". The current value is " + Alpha);
        }
        this.lat = lat;
        this.lon = lon;
        this.Theta =   Math.PI * (Theta / 180.0);
    }

    // # xp, yp: camera coordinates.
    // # The return values are local coordinates
    CameraToLocalCoordinates(xp, yp) {
        var OC1 = this.Hc * Math.tan(this.Alpha - this.BetaV / 2);
        var AC1 = this.Hc / Math.cos(this.Alpha - this.BetaV / 2.0);
        var AC = AC1 * Math.cos(this.BetaV / 2);
        var B1C1 = AC * Math.tan(this.BetaH / 2);
        var K = 2 * B1C1 / this.W;
        var Xxpyp = K * xp ;
        var Yxpyp = OC1 + ( K * this.H / 2 + K * yp ) * Math.cos(this.Alpha);
        var Zxpyp = ( K * this.H / 2 + K * yp ) * Math.sin(this.Alpha);
        var x = Xxpyp * ( -this.Hc / (Zxpyp - this.Hc));
        var y = Yxpyp * ( -this.Hc / (Zxpyp - this.Hc));
        return { x:x, y:y };
    }

    // # xp range: (- H / 2, + W / 2)
    // # yp range: (- H / 2, + W / 2)
    // # the return values are latitude and longitude
    CameraToGlobalCoordinates(xp, yp) {
        // # Radius of earth is 6378100.0 meters
        var Re = 6378100.0;
        var lo = this.CameraToLocalCoordinates(xp, yp);
        var xl = lo.x;
        var yl = lo.y;
        var xe = xl * Math.cos(this.Theta) - yl * Math.sin(this.Theta);
        var yn = yl * Math.cos(this.Theta) + xl * Math.sin(this.Theta);
        var lat = this.lat + (yn / Re * 180.0 / Math.PI);
        var lon = this.lon + (xe / Re * 180.0 / Math.PI);
        return { lat:lat, lon:lon };
    }
}

var heatmap={
    create: function (ctx, sensor_location) {
        ctx.heatmap=L.heatLayer(sensor_location, {radius: 10, blur: 5} );
    },
    update: function (layer, ctx, zoom, sensor) {
        var camera=new CameraProjection(
            sensor._source.resolution.width,
            sensor._source.resolution.height,
            sensor._source.mnth,
            sensor._source.alpha,
            sensor._source.fovv,
            sensor._source.fovh,
            sensor._source.location.lat,
            sensor._source.location.lon,
            sensor._source.theta
        );
        apiHost.search("analytics",'sensor="'+sensor._id+'" and objects.detection:* and '+settings.heatmap_query(),sensor._source.office,100).then(function (arecords) {
            var latlngs = [];
            $.each(arecords.response, function( keya, a ) {
                var w = a._source.resolution.width;
                var h = a._source.resolution.height;
                $.each(a._source.objects, function( keyo, o ) {
                    // relative to left-top corner
                    var xi = w * (o.detection.bounding_box.x_min + o.detection.bounding_box.x_max) / 2.0;
                    var yi = h * (o.detection.bounding_box.y_min + o.detection.bounding_box.y_max) / 2.0;

                    // the origin is the center of the picture. x: from left to right, y: from bottom to top
                    var xp = xi - w / 2.0;
                    var yp = yi - h / 2.0;
                    var lo = camera.CameraToGlobalCoordinates(xp, yp);
                    latlngs.push([lo.lat, lo.lon, 0.1]);
                });
            });
            if (latlngs.length==0) {
                ctx.heatmap.remove(); 
            } else {
                ctx.heatmap.setLatLngs(latlngs);
		        if(!layer.hasLayer(ctx.heatmap)) ctx.heatmap.addTo(layer);
            }
        }).catch(function () {
            ctx.heatmap.remove();
        });
    },
    close: function (ctx) {
        ctx.heatmap.remove();
    },
};
