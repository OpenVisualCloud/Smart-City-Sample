
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

    "hint-search-datetime": "日期检索: VAR>MM/DD/YYYY, VAR<hh/mm/ss[.uuu], 或者 VAR>=MM/DD/YYYY hh/mm/ss[.uuu], 这里hh 使用24 小时表示.",
    "hint-search-number": "数字检索：区间 {} VAR=公式 或者 VAR&gt;=公式",
    "hint-search-string": '字串检索: VAR:"字串" 或者VAR="字串"',
    "hint-search-location": "经纬度检索: VAR:[&lt;维度&gt;,&lt;经度&gt;] 或者 VAR:[&lt;纬度&gt;,&lt;经度&gt;,&lt;距离半径&gt;]",
    "hint-search-ip": "网络地址检索: VAR=192.168.1.0 或者 VAR=192.168.1.0/16",

    "cpu": "处理器",
    "mem": "内存",
    "disk": "磁盘",

    "vehicle": "车辆",
    "person": "人",
    "car": "汽车",
    "bicycle": "自行车",
    "bus": "公共汽车",
    "trunk": "卡车",

    "recording-unavailable": "录像暂时没有",
    "recording-loading": "载入...",

    "b/s": "b/s",
    "kb/s": "Kb/s",
    "mb/s": "Mb/s",
    "gb/s": "Gb/s",

    "traffic planning": "道路交通",
    "stadium services": "体育场馆",
    
    "connection info": "链接信息",
    "density estimation": "热成像图",
    "statistics histogram": "统计曲线",
    "preview clips": "录像预览",
    "Scrolling Alerts": "警报信息",

    "camera": "摄像机",
    "ip_camera": "网络摄像机",

    "error": "连接出错",
    "workload title": "{} 负载",

    "active": "运行中",
    "processing": "运行中",
    "N/A": "无",
    "office online": "工作正常",
    "office offline": "工作异常",
    "connection error": "连接出错",
    "central office": "数据库",
};

