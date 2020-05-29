
text={
    format: function (msg, args) {
        for (var i in args)
            msg=msg.replace('{}',args[i]);
        return msg;
    },
    translate: function (msg) {
        return (msg in text)?text[msg]:msg;
    },

    "hint-search-datetime": "Search date time: VAR>MM/DD/YYYY, VAR<hh/mm/ss[.uuu], or VAR>=MM/DD/YYYY hh/mm/ss[.uuu], where hh is in 24 hours.",
    "hint-search-number": "Search numbers {}: VAR=&lt;expr&gt; or VAR&gt;=&lt;expr&gt;",
    "hint-search-string": 'Search strings: VAR:"string" or VAR="string"',
    "hint-search-location": "Search geometric locations: VAR:[&lt;lat&gt;,&lt;lon&gt;] or VAR:[&lt;lat&gt;,&lt;lon&gt;,&lt;radius&gt;]",

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
};

