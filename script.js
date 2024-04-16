var socket = new WebSocket("ws://localhost:8080/video-events");

socket.onopen = function(event) {
  console.log("WebSocket connection established.");
};


function playVideo() {
  var video = document.getElementById('videoPlayer');
  var button = document.getElementById('playButton');
  video.style.display = 'block';
  button.style.display = 'none';
  video.play();
  video.onended = function() {
    video.style.display = 'none';
    document.getElementById('loadingMessage').style.display = 'block';
    var message = { event: 'videoEnded' };
    socket.send(JSON.stringify(message));
  }
}


