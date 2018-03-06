let loadFile = function(event) {
  let output = document.getElementById('upload');
  output.src = URL.createObjectURL(event.target.files[0]);
} 
