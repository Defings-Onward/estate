// export {sendSignal, createOfferer, addLocalTracks, createAnswerer}
// import { username, mapPeers } from "./main.js";
// var username = JSON.parse(localStorage.getItem('username'))
console.log('In main.js')
var mapPeers = {};
var username = localStorage.getItem("username");

if (!username) {
    // If username is missing, ask again or send user back
    username = prompt("Enter your username:");
    
    if (!username) {
        alert("Username is required!");
        window.location.href = ""; // Redirect back
        
    }
    
    sessionStorage.setItem("username", username); // Store username
}
localStorage.removeItem("username")
console.log("Username:", username);


var webSocket;

function webSocketOnMessage(event) {
    var parsedData = JSON.parse(event.data);
    var peerUsername = parsedData['peer'];
    var action = parsedData['action'];
    console.log("Message Triggered but not completed")
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
    console.log("Message Triggered")
}


function startWebSocketConnection() {

    if(username == '') {
        return;
    }
    // localStorage.setItem('username', JSON.stringify(username))
    
    
    
    
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

        sendSignal('new-peer', '', 'what_a_channel')
        
        
    });
    webSocket.addEventListener('message', webSocketOnMessage);
    webSocket.addEventListener('close', (e) => {
        console.log('Connection Closed!')
    });
    webSocket.addEventListener('error', (e) => {
        console.log('Error Detected!', e.data)
    });


}


var localStream = new MediaStream();

const constraints = {
    'video': true,
    'audio': true
}

const localVideo = document.querySelector('#local-video');
const btnToggleAudio = document.querySelector('#btn-toggle-audio');
const btnToggleVideo = document.querySelector('#btn-toggle-video');

var userMedia = navigator.mediaDevices.getUserMedia(constraints)
    .then(stream => {
        localStream = stream;
        localVideo.srcObject = localStream;
        localVideo.muted = true;
        var audioTracks = stream.getAudioTracks();
        var videoTracks = stream.getVideoTracks();
        audioTracks[0].enabled = true;
        videoTracks[0].enabled = true;
        btnToggleAudio.addEventListener('click', () =>{
            audioTracks[0].enabled = !audioTracks[0].enabled;
            if(audioTracks[0].enabled){
                btnToggleAudio.innerHTML = "Mic Off"
                return;
            }
            btnToggleAudio.innerHTML = "Mic On"
        })
        btnToggleVideo.addEventListener('click', () =>{
            videoTracks[0].enabled = !videoTracks[0].enabled;
            if(videoTracks[0].enabled){
                btnToggleAudio.innerHTML = "Video Off"
                return;
            }
            btnToggleVideo.innerHTML = "Video Out"
        })    
    })
    .catch(error => {
        console.log("Error accessing media devices", error)
    });
    
    

function sendSignal(action, sdp, receiver_channel_name) {
    
    var jsonStr = JSON.stringify({
        'peer': username,
        'action': action,
        'message': {
            'sdp': sdp,
            'receiver_channel_name': receiver_channel_name
        }
    })

    webSocket.send(jsonStr)
    
    
}
function createOfferer(peerUsername, receiver_channel_name) {
    var peer = new RTCPeerConnection(null);
    addLocalTracks(peer);
    var dc = peer.createDataChannel('channel')
    dc.addEventListener('open', () => {
        console.log(' DC Connection opened!')
    });
    dc.addEventListener('message', dcOnMessage)
    var remoteVideo = createVideo(peerUsername);
    setOnTrack(peer, remoteVideo)
    mapPeers[peerUsername] = [peer, dc];
    peer.addEventListener('iceconnectionstatechange', () => {
        var iceConnectionState = peer.iceConnectionState;
        if(iceConnectionState === 'failed' || iceConnectionState === 'disconnected' || iceConnectionState === 'closed'){
            delete mapPeers[peerUsername];
            if(iceConnectionState != 'closed') {
                peer.close();

            }
            removeVideo(remoteVideo);
            console.log("removed video")
        }
    });

    peer.addEventListener('icecandidate', (event) => {
        if(event.candidate){
            console.log('New Ice candidate: ', JSON.stringify(peer.localDescription));
            return;
        }
        sendSignal(
            'new-offer', peer.localDescription,
                receiver_channel_name
            
        )
    })

    peer.createOffer()
    .then(o => peer.setLocalDescription(o))
    .then(() => {
        console.log('local description set successfully')
    })
    
}
function createAnswerer(offer, peerUsername, receiver_channel_name){
    var peer = new RTCPeerConnection(null);
    addLocalTracks(peer);
    
    var remoteVideo = createVideo(peerUsername);
    setOnTrack(peer, remoteVideo);
    peer.addEventListener('datachannel', e => {
        peer.dc = e.channel;
        peer.dc.addEventListener('open', () => {
            console.log('Peer Connection opened!')
        });
        peer.dc.addEventListener('message', dcOnMessage);
    })
    
    peer.addEventListener('iceconnectionstatechange', () => {
        var iceConnectionState = peer.iceConnectionState;
        if(iceConnectionState === 'failed' || iceConnectionState === 'disconnected' || iceConnectionState === 'closed'){
            delete mapPeers[peerUsername];
            if(iceConnectionState != 'closed') {
                peer.close();

            }
            removeVideo(remoteVideo);
        }
    });

    peer.addEventListener('icecandidate', (event) => {
        if(event.candidate){
            console.log('New Ice candidate: ', JSON.stringify(peer.localDescription));
            return;
        }
        sendSignal(
            'new-answer',
                peer.localDescription,
                receiver_channel_name
            
        )
    })
    peer.setRemoteDescription(offer)
    .then(() => {
        console.log('Remote description set successfully for %s.', peerUsername)
        return peer.createAnswer();
    })
    .then(a => {
        console.log("Answer Created!");
        peer.setLocalDescription(a)
    })

    // peer.createOffer()
    // .then(o => peer.setLocalDescription(o))
    // .then(() => {
    //     console.log('local description set successfully')
    // })
    
}
function addLocalTracks(peer) {
    localStream.getTracks().forEach(track => {
        peer.addTrack(track, localStream)
    })
    return
}
var messageList = document.querySelector('#message-list');
function dcOnMessage(event) {
 var message = event.data;
 var li = document.createElement('div');
 li.appendChild(document.createTextNode(message));
 messageList.appendChild(li)
}

function createVideo(peerUsername) {
    var videoContainer = document.querySelector('.bad-vido');

    var remoteVideo = document.createElement('video');

    remoteVideo.id = peerUsername + '-video';
    remoteVideo.autoplay = true;
    remoteVideo.playsInline = true;

    
    var videoWrapper2 = document.createElement('div');
    videoWrapper2.className = 'act-vid'
    videoContainer.appendChild(videoWrapper2);
    videoWrapper2.appendChild(remoteVideo)
    console.log("remotevideo")
    
    return remoteVideo;
}
function setOnTrack(peer, remoteVideo){
    var remoteStream = new MediaStream();
    navigator.mediaDevices.getUserMedia(constraints)
        .then(stream => {
            localStream = stream;
            remoteVideo.srcObject = remoteStream;
            remoteVideo.muted = true;
                
        })
        .catch(error => {
            console.log("Error accessing media devices", error)
        });
    remoteVideo.srcObject = remoteStream;

    peer.addEventListener('track', async (event) => {
        remoteStream.addTrack(event.track, remoteStream)
    })
    console.log("video " + peer + " streamed")
}

function removeVideo(remoteVideo){
    var videoWrapper = video.parentNode;
    videoWrapper.parentNode.removeChild(videoWrapper)
}

startWebSocketConnection();
