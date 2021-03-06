let nav = document.getElementById('navbar');
let mobileNav = document.getElementById('mobile-nav');
window.addEventListener('scroll', function (e) {
  if (document.documentElement.scrollTop
    || document.body.scrollTop > window.innerHeight) {
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

let listaGoles = document.getElementsByClassName('gol-container');
if (listaGoles) {
  for(let i = 0; i < listaGoles.length; i++) {
    let el = listaGoles[i];
    for(let j = 0; j < el.getAttribute('data-value'); j++) {
      el.innerHTML += '<div class="gol"></div>'
    }
  }
}

let partidosJugados = document.getElementById('partidos');
let golesAnotados = document.getElementById('golesAnotados');
if (partidosJugados && golesAnotados) {
  partidosJugados = partidosJugados.getAttribute('data-value');
  partidosJugadosE = partidosJugados.slice(0, partidosJugados.indexOf(' '));
  partidosJugadosJ = partidosJugados.slice(partidosJugados.lastIndexOf(' ')+1);
  golesAnotados = golesAnotados.getAttribute('data-value');
  golesAnotadosE = golesAnotados.slice(0, golesAnotados.indexOf(' '));
  golesAnotadosJ = golesAnotados.slice(golesAnotados.lastIndexOf(' ')+1);
  golesAnotadosJ === 'None' ? (golesAnotadosJ = 0) : null;
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
          circle.setText('0');
        } else {
          circle.setText(value);
        }
      }
    });
    bar2.animate(golesAnotadosE);
    bar2.text.style.color = 'rgba(3,27,78,.7)';
  };
}


let elements = document.getElementsByClassName("activator");

for(var i=0; i < elements.length;i++) {
  let element = elements[i];
  element.addEventListener("click",  function() {
    this.parentNode.classList.add('big');
  });
}

let closeElements = document.getElementsByClassName("close");

for(var i=0; i < closeElements.length;i++) {
  let element = closeElements[i];
  console.log(element)
  element.addEventListener("click",  function() {
    this.parentNode.parentNode.classList.remove('big');
  });
}
