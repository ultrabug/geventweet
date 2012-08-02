var txt = document.getElementById("tweet-list");
var msg = document.getElementById("message");
var start = document.getElementById("start");
var stop = document.getElementById("stop");

var disabled = false;

function reset() {
	if (!disabled) { txt.innerHTML = ''; }
}

function oops() {
	msg.innerHTML = '<div class="alert alert-error"><b>Oops</b> we got disconnected from server, hold on...</div>';
}

function pause() {
	msg.innerHTML = '<div class="alert alert-warning">Ignoring the tweeting bird for now.</div>';
}

function feeding() {
	msg.innerHTML = '<div class="alert alert-info"><b>NB:</b> tweets are cleared when we see a # in the text.</div>';
}

$(function() {

	var socket = io.connect();

	socket.on('connect',    function()    { socket.emit('get_tweets'); feeding(); });
	socket.on('reset',      function()    { reset();                              });
	socket.on('disconnect', function()    { socket = io.connect(); oops();        });

	socket.on('tweet', function (json) {
		var data = JSON.parse(json);
		if (!disabled) {
			txt.innerHTML = '<div><span class="label label-info">'+data['user']+'</span> '+data['text']+'</div>' + txt.innerHTML;
		}
    });

	start.onclick = function() { disabled = false; feeding(); stop.className = "btn btn-danger"; start.className += " disabled";  };
	stop.onclick  = function() { disabled = true;  pause();  start.className = "btn btn-success"; stop.className += " disabled";  };

});
