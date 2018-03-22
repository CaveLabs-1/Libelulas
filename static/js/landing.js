let nav = document.getElementById('navbar');
let mobileNav = document.getElementById('mobile-nav');
console.log(mobileNav);
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
