let loadFile = function(event) {
  let output = document.getElementById('upload');
  output.src = URL.createObjectURL(event.target.files[0]);
}

function hideMessage() {
  setTimeout(() => {
    document.getElementById('message').style.animationPlayState = 'running'
  }, 1000);
};


document.getElementById('message')
? hideMessage()
: null;
