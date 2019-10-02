var gamePGN;

function parsePgnText() {
    var pgnString = document.getElementById("PgnInput").value;
    if(!pgnGameFromPgnText(pgnString)) {
       return;
    }
    setPgnString(pgnString);
    document.getElementById("Game").classList.add("visible");
    document.getElementById("NewGame").classList.add("visible");
    // Restart pgn4web after receiving pgn
    start_pgn4web();
    LoadGameHeaders();
    // After skimming pgn4web code for a long time I couldn't find
    // the native way to reinitialize the population of tags
    // so I did in manually
    document.getElementById("GameDate").innerText = gameDate[0];
    document.getElementById("GameWhite").innerText = gameWhite;
    document.getElementById("GameBlack").innerText = gameBlack;
    document.getElementById("GameEvent").innerText = gameEvent;
    // To make it applicable for the eco code parser
    gamePGN = pgnString;
    populateVariation();
    document.getElementById("UploadForm").classList.add("hidden");
}
