
text={
    "hint-search-datetime": "日期检索: VAR>MM/DD/YYYY, VAR<hh/mm/ss[.uuu], 或者VAR>=MM/DD/YYYY hh/mm/ss[.uuu], 这里hh 使用24 小时表示.",
    "hint-search-number": "数字检索：区间{}: VAR=&lt;公式&gt;或者VAR&gt;=&lt;公式&gt;",
    "hint-search-string": '字串检索: VAR:"字串"或者VAR="字串"',
    "hint-search-location": "经纬度检索: VAR:[&lt;维度&gt;,&lt;经度&gt;] or VAR:[&lt;纬度&gt;,&lt;经度&gt;,&lt;距离半径&gt;]",

    format: function (msg, args) {
        for (var i in args)
            msg=msg.replace('{}',args[i]);
        return msg;
    }
};
