
text={
    "hint-search-datetime": "Search date time: VAR>MM/DD/YYYY, VAR<hh/mm/ss[.uuu], or VAR>=MM/DD/YYYY hh/mm/ss[.uuu], where hh is in 24 hours.",
    "hint-search-number": "Search numbers {}: VAR=&lt;expr&gt; or VAR&gt;=&lt;expr&gt;",
    "hint-search-string": 'Search strings: VAR:"string" or VAR="string"',
    "hint-search-location": "Search geometric locations: VAR:[&lt;lat&gt;,&lt;lon&gt;] or VAR:[&lt;lat&gt;,&lt;lon&gt;,&lt;radius&gt;]",

    format: function (msg, args) {
        for (var i in args)
            msg=msg.replace('{}',args[i]);
        return msg;
    }
};
