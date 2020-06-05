
text={
    format: function (msg) {
        msg=text.translate(msg);
        for (var i=1;i<arguments.length;i++)
            msg=msg.replace("{}",arguments[i]);
        return msg;
    },
    translate: function (msg) {
        return (msg in text)?text[msg]:msg;
    },

    "hint-search-datetime": "Search date time: VAR>MM/DD/YYYY, VAR<hh/mm/ss[.uuu], or VAR>=MM/DD/YYYY hh/mm/ss[.uuu], where hh is in 24 hours.",
    "hint-search-number": "Search numbers {}: VAR=&lt;expr&gt; or VAR&gt;=&lt;expr&gt;",
    "hint-search-string": 'Search strings: VAR:"string" or VAR="string"',
    "hint-search-location": "Search geometric locations: VAR:[&lt;lat&gt;,&lt;lon&gt;] or VAR:[&lt;lat&gt;,&lt;lon&gt;,&lt;radius&gt;]",
    "hint-search-ip": 'Search IP address: VAR=192.168.1.0 or VAR=192.168.1.0/16',

    "cpu": "cpu",
    "mem": "mem",
    "disk": "disk",

    "vehicle": "vehicle",
    "person": "person",
    "car": "car",
    "bicycle": "bicycle",
    "bus": "bus",
    "trunk": "trunk",

    "recording-unavailable": "Recording Unavailable",

    "b/s": "b/s",
    "kb/s": "Kb/s",
    "mb/s": "Mb/s",
    "gb/s": "Gb/s",

    "traffic planning": "Traffic Planning",
    "stadium services": "Stadium Services",
    
    "connection info": "Connection Info",
    "density estimation": "Density Estimation",
    "statistics histogram": "Statistics Histogram",
    "preview clips": "Preview Clips",
    "Scrolling Alerts": "Scrolling Alerts",

    "camera": "Camera",
    "ip_camera": "IP Camera",

    "workload title": "{} Workload",
    "N/A": "N/A",
};

