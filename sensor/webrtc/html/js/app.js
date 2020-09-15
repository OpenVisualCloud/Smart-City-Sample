
function subscribeRoom(video, roomid, streamid) {
    var conference=new Owt.Conference.ConferenceClient();

    $.post("/api/tokens",{ room: roomid }).then(function (token) {
        conference.join(token).then(function (r) {
            r.remoteStreams.forEach(function (stream) {
                if (stream.id!=streamid) return;

                conference.subscribe(stream, { audio: false}).then(function (subscription) {
                    video.get(0).srcObject = stream.mediaStream;
                }, function (e) {
                    console.error('Subscription failed:', e);
                });
            });
        }, function (e) {
            console.error('Connection failed:', e);
        });
    });

    return conference;
}
    
window.onload = function() {
    var roomid, streamid;

    var kvs=window.location.search.substring(1).split('&');
    for (var i = 0; i < kvs.length; i++) {
        var kv=kvs[i].split('=');
        if (kv[0] === "roomid") roomid=decodeURIComponent(kv[1]);
        if (kv[0] === "streamid") streamid=decodeURIComponent(kv[1]);
    }

    var conference=subscribeRoom($("video"), roomid, streamid);
    window.onbeforeunload = function(event) {
        conference.leave()
    };
};

