window.addEventListener('scroll', function (e) {
  let nav = document.getElementById('navbar');
  if (document.documentElement.scrollTop || document.body.scrollTop > window.innerHeight) {
    nav.classList.add('colored');
    nav.classList.remove('transparent');
  } else {
    nav.classList.add('transparent');
    nav.classList.remove('colored');
  }
});
