console.log('In main.js')
var mapPeers = {};
var usernameInput = document.querySelector('.username')
var btnJoin = document.querySelector('.btn-main')

var username;

var webSocket;

function webSocketOnMessage(event) {
    var parsedData = JSON.parse(event.data);
    var peerUsername = parsedData['peer'];
    var action = parsedData['action'];

    if (username == peerUsername) {
        return;
    }
    var receiver_channel_name = parsedData['message']['receiver_channel_name'];

    if (action == 'new-peer') {
        createOfferer(peerUsername, receiver_channel_name);
        return;
    }
    if (action == 'new-offer'){
        var offer = parsedData['message']['sdp']
        createAnswerer(offer, peerUsername, receiver_channel_name);
        return;
    }
    if(action == 'new-answer') {
        var answer = parsedData['message']['sdp'];
        var peer = mapPeers[peerUsername][0];
        peer.setRemoteDescription(answer);
        return;
    }
    console.log('message: ', message)
}

btnJoin.addEventListener('click', () => {
    username = usernameInput.value;

    if(username == '') {
        return;
    }
    // localStorage.setItem('username', JSON.stringify(username))
    
    usernameInput.disabled = true;

    btnJoin.disabled = true;
    

    var loc = window.location;
    var wsStart = 'ws://';

    if(loc.protocol == 'https:'){
        wsStart = 'wss://';
    }

    var endPoint = wsStart + loc.host + loc.pathname;
    console.log('endpoint', endPoint);

    webSocket = new WebSocket(`"${endPoint}"`);

    webSocket.addEventListener('open', (e) => {
        console.log('Connection Opened!')

        sendSignal('new-peer', {})
    });
    webSocket.addEventListener('message', webSocketOnMessage);
    webSocket.addEventListener('close', (e) => {
        console.log('Connection Closed!')
    });
    webSocket.addEventListener('error', (e) => {
        console.log('Error Detected!', e.data)
    });


})

