// --- Config --- //
var purecookieTitle = "[GDPR]"; // Title
var purecookieDesc = "By using PSINDB you accept the Privacy Notice in compliance with Europe’s new General Data Protection Regulation (GDPR) that applies since 25 May 2018. Read the"; // Description
var purecookieLink = '<a href="/privacy-policy" target="_blank">Privacy notes</a>.'; // Cookiepolicy link
var purecookieButton = "Understood"; // Button text
// ---        --- //


function pureFadeIn(elem, display){
  var el = document.getElementById(elem);
  el.style.opacity = 0;
  el.style.display = display || "block";

  (function fade() {
    var val = parseFloat(el.style.opacity);
    if (!((val += .02) > 1)) {
      el.style.opacity = val;
      requestAnimationFrame(fade);
    }
  })();
};
function pureFadeOut(elem){
  var el = document.getElementById(elem);
  el.style.opacity = 1;

  (function fade() {
    if ((el.style.opacity -= .02) < 0) {
      el.style.display = "none";
    } else {
      requestAnimationFrame(fade);
    }
  })();
};

function setCookie(name,value,days) {
    var expires = "";
    if (days) {
        var date = new Date();
        date.setTime(date.getTime() + (days*24*60*60*1000));
        expires = "; expires=" + date.toUTCString();
    }
    document.cookie = name + "=" + (value || "")  + expires + "; path=/";
}
function getCookie(name) {
    var nameEQ = name + "=";
    var ca = document.cookie.split(';');
    for(var i=0;i < ca.length;i++) {
        var c = ca[i];
        while (c.charAt(0)==' ') c = c.substring(1,c.length);
        if (c.indexOf(nameEQ) == 0) return c.substring(nameEQ.length,c.length);
    }
    return null;
}
function eraseCookie(name) {
    document.cookie = name+'=; Max-Age=-99999999;';
}

function cookieConsent() {
  if (!getCookie('purecookieDismiss')) {
	var cookieContainer = document.createElement('DIV')
    var cookieTitleContainer = document.createElement('DIV')
    var cookieTitle = document.createElement('A')
    var cookieDescriptionContainer = document.createElement('DIV')
    var cookieDescription = document.createElement('P')
    var cookieButtonContainer = document.createElement('DIV')
    var cookieButton = document.createElement('A')
    var cookieLink = document.createElement('A')

    cookieContainer.classList.add('cookieConsentContainer')
    cookieContainer.setAttribute('id', 'cookieConsentContainer')
    cookieLink.setAttribute('href', '/privacy-policy')
    cookieLink.setAttribute('target', '_blank')
    cookieTitleContainer.classList.add('cookieTitle')
    cookieDescriptionContainer.classList.add('cookieDesc')
    cookieButtonContainer.classList.add('cookieButton')
    cookieTitle.innerText = purecookieTitle;
    cookieDescription.innerText = purecookieDesc
    cookieButton.innerText = purecookieButton
    cookieLink.innerText = 'Privacy notes'
    cookieButton.addEventListener('click', function () {
      purecookieDismiss();
    })

    cookieButtonContainer.appendChild(cookieButton);
    cookieDescriptionContainer.appendChild(cookieDescription);
    cookieDescriptionContainer.appendChild(cookieLink);
    cookieTitleContainer.appendChild(cookieTitle);

    cookieContainer.appendChild(cookieTitleContainer)
    cookieContainer.appendChild(cookieDescriptionContainer)
    cookieContainer.appendChild(cookieButtonContainer)

    document.getElementsByTagName('BODY')[0].appendChild(cookieContainer)
      pureFadeIn("cookieConsentContainer");
  }
}


function purecookieDismiss() {
  setCookie('purecookieDismiss','1',7);
  pureFadeOut("cookieConsentContainer");
}

// window.onload = function() { cookieConsent(); };

$(document).ready(function(){
    cookieConsent();
});