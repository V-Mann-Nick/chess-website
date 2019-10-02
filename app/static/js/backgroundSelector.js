/*
*  This document provides functions for the BackgroundChoice window.
*  Required files:
*      1) *.html of this project
*  @author: Nicklas Sedlock
*/

/*
* PURPOSE : set up an event listener to handle opening and closing of bg-BackgroundChoice window.
*/
function setupEventListener() {
    var BackgroundChoice = document.querySelector("#BackgroundChoice");
    document.addEventListener("click", function(event) {
        if(event.target.closest("#Settings")) {
            BackgroundChoice.classList.toggle("visible");
        } else if(event.target.closest("#BackgroundChoice")) {
            return;
        } else if(BackgroundChoice.classList.contains("visible")) {
            BackgroundChoice.classList.toggle("visible");
        }
    });
}


/*
* PURPOSE : Change background image to the specefied number.
*  PARAMS : bgNumber - background number
*/
function changeMainBackground(bgNumber) {
    body = document.querySelector("body")
    body.style.setProperty("background-image", "url('/static/images/backgrounds/body_background_" + bgNumber + ".jpg')");
    setCookie("background", bgNumber.toString(), 1)
}


function setCookie(cname, cvalue, exdays) {
  var d = new Date();
  d.setTime(d.getTime() + (exdays*24*60*60*1000));
  var expires = "expires="+ d.toUTCString();
  document.cookie = cname + "=" + cvalue + ";" + expires + ";path=/";
}


function getCookie(cname) {
  var name = cname + "=";
  var decodedCookie = decodeURIComponent(document.cookie);
  var ca = decodedCookie.split(';');
  for(var i = 0; i <ca.length; i++) {
    var c = ca[i];
    while (c.charAt(0) == ' ') {
      c = c.substring(1);
    }
    if (c.indexOf(name) == 0) {
      return c.substring(name.length, c.length);
    }
  }
  return "";
}


function checkCookie(cname) {
    var cookie = getCookie(cname);
    if(cookie != "") {
        return true;
    } else {
        return false;
    }
}
