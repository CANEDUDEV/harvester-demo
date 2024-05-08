var socket = new WebSocket("ws://localhost:8080/video-events");

socket.onopen = function(event) {
  restartDemo();
};

socket.onmessage = function(event) {
  if (event.data === "connected") {
    playVideo();
  }

  if (event.data === "disconnected") {
    restartDemo();
  }

  if (event.data.startsWith("identified")) {
    id = event.data.split(":")[1];
    updateIdentifier(id);
  }
}


function restartDemo() {
  document.getElementById('loadingMessage').style.display = 'none';
  document.getElementById('waitingMessage').style.display = 'block';
  socket.send("connect");
}

function playVideo() {
  document.getElementById('waitingMessage').style.display = 'none';
  document.getElementById('finishButton').style.display = 'block';
  var video = document.getElementById('videoPlayer');
  video.currentTime = 0;
  video.style.display = 'block';
  video.play();
  socket.send("identify");
}

function stopVideo() {
  document.getElementById('finishButton').style.display = 'none';
  document.getElementById('loadingMessage').style.display = 'block';
  var video = document.getElementById('videoPlayer');
  video.pause();
  video.style.display = 'none';
  socket.send("disconnect");
}

function updateIdentifier(id) {
  document.getElementById('finishButton').innerText = `Press to finish harvesting from cart ${id}`;
}
