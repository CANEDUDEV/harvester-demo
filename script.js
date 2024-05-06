var socket = new WebSocket("ws://localhost:8080/video-events");

socket.onopen = function(event) {
  console.log("WebSocket connection established.");
};

socket.onmessage = function(event) {
  if (event.data === "disconnected") {
    restartDemo();
  }
}

function restartDemo() {
  document.getElementById('loadingMessage').style.display = 'none';
  document.getElementById('playButton').style.display = 'block';
}

function playVideo() {
  document.getElementById('playButton').style.display = 'none';
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
  var message = { event: 'videoEnded' };
  socket.send(JSON.stringify(message));
}
