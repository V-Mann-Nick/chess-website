/*
*  This document calls functions from the pgn4web.js to configure the chess board as puzzler
*  Required files:
*      1) pgn4web.js
*      2) puzzles.html
*  @author: Nicklas Sedlock
*/

"use strict";

SetCommentsIntoMoveText(true); // no pgn comments are displayed
SetShortcutKeysEnabled(false); // no keyboard shortcuts
clearShortcutSquares("ABCDEFGH", "12345678"); // clears all square hotkeys
SetInitialGame("random"); // picks a random puzzle from pgn

/* -------------------------------------------------------------------*/
/* --------------------FUCNTION FOR ToMoveColor-----------------------*/
/* -------------------------------------------------------------------*/

/*
* PURPOSE : Manages the appearence of ToMoveColor
*/
function setToMoveColor() {
    var
        toMoveColor = document.getElementById('ToMoveColor');

    if(CurrentPly == 0) {
        toMoveColor.classList.replace('black', 'white')
        toMoveColor.innerHTML = "WEIß AM ZUG";

    } else {
        toMoveColor.classList.replace('white', 'black')
        toMoveColor.innerHTML = "SCHWARZ AM ZUG";
    }
}

/* -------------------------------------------------------------------*/
/* ---------------------FUCNTIONS FOR BUTTONS-------------------------*/
/* -------------------------------------------------------------------*/

/*
* PURPOSE : Go one move back.
*/
function moveBack() {
    if(CurrentPly > 0) {
        GoToMove(CurrentPly - 1);
    }
}

/*
* PURPOSE : Shows solution.
*/
function showSolution() {
    GoToMove(CurrentPly + 1);
    document.getElementById('TextAndResult').classList.add("visible");
    document.getElementById('ToMoveColor').classList.add("hidden");
}

/*
* PURPOSE : Switch to next puzzle.
*/
function nextPuzzle() {
    document.getElementById('TextAndResult').classList.remove("visible");
    document.getElementById('ToMoveColor').classList.remove("hidden");
    Init(Math.floor(Math.random()*numberOfGames));
    setToMoveColor();
}
