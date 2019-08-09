
$("#pg-office").on(":setup-alerts", function () {
    var update=function () {
        apiHost.search("alerts","time>now-5000",null).then(function (data) {
            var alerts=null;
            $.each(data.response,function (x,v) {
                if ("maintenance_required" in v._source) alerts="Maintenance Required";
                if ("balancing_required" in v._source) alerts="Balancing Required";
            });
            if (alerts) $("#pg-office").trigger(":alert",[alerts]);
        });
    };
    setInterval(update,10000);
}).on(":alert", function (e, message) {
    $("#header-text")[0].style="color:red";
    $("#header-alert").text(" ("+message+")");
    setTimeout(function () {
        $("#header-text")[0].style="color:#FDEDEC";
        $("#header-alert").text("");
    },2000);
});
