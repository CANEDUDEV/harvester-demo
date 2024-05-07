var socket = new WebSocket("ws://localhost:8080/video-events");

socket.onopen = function(event) {
  socket.send("connect");
};

socket.onmessage = function(event) {
  if (event.data === "connected") {
    playVideo();
  }
  if (event.data === "disconnected") {
    restartDemo();
  }
}

function restartDemo() {
  socket.send("connect");
  document.getElementById('loadingMessage').style.display = 'none';
  document.getElementById('waitingMessage').style.display = 'block';
}

function playVideo() {
  document.getElementById('waitingMessage').style.display = 'none';
  document.getElementById('finishButton').style.display = 'block';
  var video = document.getElementById('videoPlayer');
  video.currentTime = 0;
  video.style.display = 'block';
  video.play();
}

function stopVideo() {
  document.getElementById('finishButton').style.display = 'none';
  document.getElementById('loadingMessage').style.display = 'block';
  var video = document.getElementById('videoPlayer');
  video.pause();
  video.style.display = 'none';
  socket.send("disconnect");
}
