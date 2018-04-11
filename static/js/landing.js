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

// window.fbAsyncInit = function() {
//   FB.init({
//     appId            : 'your-app-id',
//     autoLogAppEvents : true,
//     xfbml            : true,
//     version          : 'v2.12'
//   });
//   FB.api('447400552307374?fields=albums.fields(photos.fields(source))', function(response) {
//     console.log(response)
//   });
// };
//
// (function(d, s, id){
//    var js, fjs = d.getElementsByTagName(s)[0];
//    if (d.getElementById(id)) {return;}
//    js = d.createElement(s); js.id = id;
//    js.src = "https://connect.facebook.net/en_US/sdk.js";
//    fjs.parentNode.insertBefore(js, fjs);
//  }(document, 'script', 'facebook-jssdk'));

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
