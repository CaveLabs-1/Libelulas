let nav = document.getElementById('navbar');
let mobileNav = document.getElementById('mobile-nav');
window.addEventListener('scroll', function (e) {
  if (document.documentElement.scrollTop || document.body.scrollTop > window.innerHeight) {
    mobileNav.classList.add('colored');
    mobileNav.classList.remove('transparent');
    nav.classList.add('colored');
    nav.classList.remove('transparent');
  } else {
    mobileNav.classList.add('transparent');
    mobileNav.classList.remove('colored');
    nav.classList.add('transparent');
    nav.classList.remove('colored');
  }
});

let imagesDiv = document.getElementById('imagesDiv')
var xhr = new XMLHttpRequest();
xhr.open("GET", "https://graph.facebook.com/447400552307374?fields=albums.fields(photos.fields(source))&access_token=EAACEdEose0cBAPggV2Sv96dkcMbZAVAr0EyHOqBG9RkACwcgQKvw9PVxvTHCwaqrDz6ZBzanr4qZBrDGEfLFphqFZCEORHr856wSdmu0a4dXNfExRLJGs7SK9TpPxY8QSF4vkcQhSnQIjW6uGsmOIZB0x8l2dYe3xiwcKCDbIjLcP7BbNLAfhUGAIwW0mygBvmxpctpLZCSgZDZD", true);
xhr.onload = function (e) {
  if (xhr.readyState === 4) {
    if (xhr.status === 200) {
      let photos = JSON.parse(xhr.response);
      photos = photos.albums.data;
      for(let i = 0; i < photos.length; i++) {
        for(let j = 0; j < photos[i].photos.data.length; j++) {
          imagesDiv.innerHTML += '<img src='+photos[i].photos.data[j].source+' />'
        }
      }
    } else {
      console.error(xhr.statusText);
    }
  }
};
xhr.onerror = function (e) {
  console.error(xhr.statusText);
};
xhr.send(null);

let partidosJugados = document.getElementById('partidos');
let golesAnotados = document.getElementById('golesAnotados');
if (partidosJugados && golesAnotados) {
  partidosJugados = partidosJugados.getAttribute('data-value');
  partidosJugadosE = partidosJugados.slice(0, partidosJugados.indexOf(' '));
  partidosJugadosJ = partidosJugados.slice(partidosJugados.lastIndexOf(' ')+1);
  golesAnotados = golesAnotados.getAttribute('data-value');
  golesAnotadosE = golesAnotados.slice(0, golesAnotados.indexOf(' '));
  golesAnotadosJ = golesAnotados.slice(golesAnotados.lastIndexOf(' ')+1);
  window.onload = function onLoad() {
    var bar = new ProgressBar.Circle('#partidos', {
      color: '#009CDE',
      strokeWidth: 4,
      trailWidth: 1,
      easing: 'easeInOut',
      duration: 1400,
      text: {
        autoStyleContainer: false
      },
      from: { color: '#009CDE', width: 4 },
      to: { color: '#009CDE', width: 4 },
      step: function(state, circle) {
        circle.path.setAttribute('stroke', state.color);
        circle.path.setAttribute('stroke-width', state.width);

        var value = partidosJugadosJ;
        if (value === 0) {
          circle.setText('');
        } else {
          circle.setText(value);
        }

      }
    });
    bar.animate(partidosJugadosE);
    bar.text.style.color = 'rgba(3,27,78,.7)';
    var bar2 = new ProgressBar.Circle('#golesAnotados', {
      color: '#009CDE',
      strokeWidth: 4,
      trailWidth: 1,
      easing: 'easeInOut',
      duration: 1400,
      text: {
        autoStyleContainer: false
      },
      from: { color: '#009CDE', width: 4 },
      to: { color: '#009CDE', width: 4 },
      step: function(state, circle) {
        circle.path.setAttribute('stroke', state.color);
        circle.path.setAttribute('stroke-width', state.width);

        var value = golesAnotadosJ;
        if (value === 0) {
          circle.setText('');
        } else {
          circle.setText(value);
        }
      }
    });
    bar2.animate(golesAnotadosE);
    bar2.text.style.color = 'rgba(3,27,78,.7)';
  };
}
