window.onload = function() {
  var value = document.getElementById('prog-val');

  var ws_scheme = window.location.protocol == "https:" ? "wss" : "ws";
  var ws_path = ws_scheme + '://' + window.location.host + '/ws/prog/';

  var socket = new WebSocket(ws_path);

  socket.onmessage = onmessage;
  document.getElementById('go-button').onclick = onsubmit;

  function onmessage(msg) {
    var data = JSON.parse(msg.data);
    if (data.result=='fail'){
      value.innerHTML='progress failed'
    }else{
      value.innerHTML = data.progress + '%';
    }

    if (data.state=='complete') {
      value.classList.add('complete');
    }
  }

  function onsubmit() {
    var msg = {
      action: 'start'
    };

    socket.send(JSON.stringify(msg));
  }
}
