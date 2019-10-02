/*
*  This document calls functions from the pgn4web.js to configure the chess board
*  Required files:
     1) pgn4web.js
*      2) *.html of this project
*  @author: Nicklas Sedlock
*/

"use strict";

SetCommentsIntoMoveText(true); // pgn comments are displayed
SetHighlightOption(true);
SetAutoplayDelay(1000); // milliseconds
SetShortcutKeysEnabled(false); // no keyboard shortcuts
clearShortcutSquares("ABCDEFGH", "12345678"); // clears all square hotkeys
