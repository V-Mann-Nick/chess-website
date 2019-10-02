/*
*  This document sets the color palette with help of color-thief.js
*  Checkout the project's git on: https://github.com/lokesh/color-thief
*  Required files:
*      1) color-thief.js
*      2) *.html of this project
*  @author: Nicklas Sedlock
*/

/* Integer corresponding to the index of  body_background_.jpg */
var currentBackgroundNumber = 1;

/* -------------------------------------------------------------------*/
/* -----------------FUCNTIONS CALLED IN HTML FILES--------------------*/
/* -------------------------------------------------------------------*/

/*
 * PURPOSE : This function generates main color and color palette from the selected background. It  then writes the colors to :root in the --color-variables. If wanted it also applies a opacity effect to header, navigation, main and footer by setting an inline background-color style.
 *  PARAMS : bgNumber - number which bg is switched to (null if current bg is to be used)
 *           headerOp - Opacity of Header (1 for no effect)
 *           navFootOp - Opacity of Navigation and Footer (1 for no effect)
 *           mainOp - Opacity of Main (1 for no effect)
 */
function setupColorThief(bgNumber, headerOp=1, navFootOp=1, mainOp=1) {
    if(currentBackgroundNumber != undefined && currentBackgroundNumber == bgNumber) {
        return;
    }
    var image;
    if(bgNumber == null) {
        image = new Image();
        image.crossOrigin = "Anonymous";
        var url = window.getComputedStyle(document.querySelector("body")).backgroundImage;
        image.src = url.slice(url.indexOf("images"), url.length-2);
        // If image is newly loaded wait for it to laod and then execute...
        image.onload = function() {
            configColors(image);
            configOpacity(headerOp, navFootOp, mainOp);
        }
    } else if(bgNumber < document.getElementById("BackgroundChoice").childElementCount) {
        image = document.getElementsByClassName("bgChoice")[bgNumber];
        // image is already loaded. Execute now ...
        configColors(image);
        configOpacity(headerOp, navFootOp, mainOp);
    }
    currentBackgroundNumber = bgNumber;
}

/* -------------------------------------------------------------------*/
/* ---------------HELPER FUNCTIONS NOT USED IN HTML-------------------*/
/* -------------------------------------------------------------------*/

/*
* PURPOSE : Sets the background-color value to the rgb color it has including the opacity wanted value. If values are set to 1 respective value wont be changed.
*  PARAMS : headerOp - Header Opacity to set
*           navFootOp - Navigation and Footer Opacity to set
*           mainOp - Main Opacity to set
*/
function configOpacity(headerOp, navFootOp, mainOp) {
    var
        root = document.querySelector(":root"),
        main = document.querySelector("main"),
        header = document.querySelector("header"),
        footer = document.querySelector("footer"),
        nav = document.querySelector("nav"),
        navA = document.querySelectorAll("nav a"),
        mainOldRgb, headerOldRgb, navFootOldRgb,
        mainNewRgb, headerNewRgb, navFootNewRgb;

        if(mainOp < 1) {
            mainOldRgb = window.getComputedStyle(root).getPropertyValue("--color-0");
            mainNewRgb = mainOldRgb.slice(0, mainOldRgb.length-1) + "," + mainOp + ")";
            main.style.setProperty("background-color", mainNewRgb);
        }
        if(headerOp < 1) {
            headerOldRgb = window.getComputedStyle(root).getPropertyValue("--color-0");
            headerNewRgb = headerOldRgb.slice(0, headerOldRgb.length-1) + "," + headerOp + ")";
            header.style.setProperty("background-color", headerNewRgb);
        }
        if(navFootOp < 1) {
            navFootOldRgb = window.getComputedStyle(root).getPropertyValue("--color-4");
            navFootNewRgb = navFootOldRgb.slice(0, navFootOldRgb.length-1) + "," + navFootOp + ")";
            footer.style.setProperty("background-color", navFootNewRgb);
            nav.style.setProperty("background-color", navFootNewRgb);
            for(let i = 0; i < navA.length; i++) {
                navA[i].style.setProperty("background-color", navFootNewRgb);
            }

        }
}

/*
* PURPOSE : This calls functions from the color-thief.js to first of all calculate a main color from an image (<img>). Then a color palette is calculated based on the main color. The color palette is then sorted by luminosity making 0 the least luminous and higher numbers more luminous. Then new new colors are written to :root.
*  PARAMS : image - <img>-object
*/
function configColors(image) {
    var colorThief = new ColorThief();
    var colorPalette = colorThief.getPalette(image, 5);
    var sortedColorPalette = sortColorPalette(colorPalette);

    var root = document.querySelector(":root");
    for(let i = 0; i < sortedColorPalette.length; i++) {
        root.style.setProperty("--color-" + i, rgbString(sortedColorPalette[i]));
    }
}

/*
* PURPOSE : Quick helper function to construct a string.
*  PARAMS : rgb - array of format [r, g, b]
*           opacity -  optional: include opacity in rgb.
* RETURNS : string - "rgb(r,g,b,o)"
*/
function rgbString(rgb, opacity=1.0) {
    var rgbString = "rgb(";
    for(let i = 0; i < rgb.length; i++) {
        rgbString += rgb[i];
        rgbString += ",";
    }
    if(opacity != 1.0) {
        rgbString += opacity;
    } else {
        rgbString = rgbString.substring(0, rgbString.length-1);
    }
    rgbString += ")";
    return rgbString;
}

/*
* PURPOSE : Sorts an array of colors by their luminosity.
*  PARAMS : colors - array of format [[r,g,b],[r,g,b],...]
* RETURNS : array of format [[r,g,b],[r,g,b],...]
*/
function sortColorPalette(colors) {
    var luminance = new Array(colors.length);
    for(let i = 0; i < colors.length; i++) {
        currentColor = colors[i];
        luminance[i] = (0.299*currentColor[0] + 0.587*currentColor[1] + 0.114*currentColor[2]);
    }
    luminanceWithIdx = [];
    for(let i = 0; i < colors.length; i++) {
        luminanceWithIdx.push([luminance[i], i]);
    }
    luminanceWithIdx.sort(function(left,right) {
        return left[0] < right[0] ? -1 : 1;
    });
    var sortedColors = new Array(colors.length);
    for(let i = 0; i < colors.length; i++) {
        sortedColors[i] = colors[luminanceWithIdx[i][1]]
    }
    return sortedColors;
}
