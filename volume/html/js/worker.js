
onmessage=function (e) {
    console.log("GET "+e.data);
    var web_socket=new WebSocket(e.data);
    web_socket.onclose=function() {
        console.log("websocket closed");
    };
    web_socket.onerror=function() {
        console.log("websocket error");
    };
    web_socket.onmessage=function (e) {
        postMessage(e.data);
    };
};

