const snakeColours = ["#607D8B","#E91E63","#9C27B0", "#3F51B5", "#03A9F4", "#009688", "#CDDC39", "#FFEB3B", "#FF9800", "#FF5722", "#795548"];
const snakeFaces = [":)", ":O", "xD", ":P", ">:(", "8)", ":C", ":3", ":E"]
var snakesHead = [false, true, true, true, true, true, true, true, true, true, true, true, true];

var currentSelected = 0;
var tableSize = 20;
var mouseDown = 0;  // store mouse status
var width = 0;
var height = 0;
var tableWidth = 0;
var tableHeight = 0;
var turnCounter = 0;
let interLength = 200;
var interID;
var paused = true;

var openFile = function(event) {
    var input = event.target;

    var reader = new FileReader();
    reader.onload = function(){
        var text = reader.result;
        turnData = JSON.parse(text);
        renderTurn(0)
    };
    reader.readAsText(input.files[0]);
};

function main() {  
    width = window.innerWidth - 50;
    height = window.innerHeight - 50;

    snakeColours.sort(function() { return 0.5 - Math.random() });
    snakeFaces.sort(function() { return 0.5 - Math.random() });

    tableCreate();
}

function start() {
    if (paused) {
        interID = setInterval(playTurn, interLength)
        paused = false
    } else {
        console.log("Already playing!")
    }
}
function playTurn() {
    clearCells()
    renderTurn(turnCounter)
    turnDisplay(turnCounter)
    turnCounter++
    if (turnCounter >= turnData.length) {
        clearInterval(interID);
    }
}
function turnDisplay(curTurn) {
    document.getElementById('turnDisplay').innerText = curTurn
}
function pause() {
    clearInterval(interID)
    paused = true
}
function jumpTo() {
    jumpToTurn = document.getElementById('thisTurn').value;
    console.log("Jumping to "+jumpToTurn)
    turnCounter = jumpToTurn;
    clearCells()
    renderTurn(turnCounter)
    turnDisplay(turnCounter)
}
//Update delay between turn rendering. If currently playing, call setInterval
function playbackSpeed() {
    clearInterval(interID)
    interLength = document.getElementById('playbackSpeed').value
    console.log("new delay: "+interLength)
    if (!paused) {
        interID = setInterval(playTurn, interLength)
    }
}
//Remove all colors from board
function clearCells() {

    for (let x=0; x < tableSize; x++ ) {
        for (let y=0; y < tableSize; y++) {
            let curCell = x+','+y
            document.getElementById(curCell).style.backgroundColor = "rgb(255,255,255)";
            document.getElementById(curCell).innerText = "";
        }
    }
}
//Render the colors for a specific turn
function renderTurn(turnToRender) {
    const curTurn = turnData[turnToRender]

    //Add food for new turn
    for (x in curTurn.food){
        var kibbles = curTurn.food[x];
        document.getElementById(kibbles[0]+','+kibbles[1]).style.backgroundColor = "rgb(76, 175, 80)";
    }
    //Add snakes for new turn
    for (x in curTurn.snakes){
        var curSnake = curTurn.snakes[x];
        for (k in curSnake.coords){
            var curCoord = curSnake.coords[k];
            document.getElementById(curCoord[0]+','+curCoord[1]).style.backgroundColor = snakeColours[x];
            if (k == 0) {
                document.getElementById(curCoord[0]+','+curCoord[1]).innerText = snakeFaces[x];
            }
        }
    }
}
function tableCreate() {
    
    var body = document.getElementsByTagName("body")[0];  // get body

    var tbl = document.createElement("table");  // declare table
    tbl.setAttribute("border", "1");
    tbl.setAttribute("id", "table");

    if (width > height){
        var desiredWidth = width;
        if (height < width / 2){
          tableWidth = tbl.style.width = height;
          tableHeight = tbl.style.height = height;
        } else {
          tableWidth = tbl.style.width = width / 2;
          tableHeight = tbl.style.height = (width / 2);
        }
    } else {
        tableWidth = tbl.style.width = width;
        tableHeight = tbl.style.height = (width);
    }

    var tbdy = document.createElement("tbody");  // declare body

    for (var row = 0; row < tableSize; row++) {  // for table size

        var tr = document.createElement("tr");  // declare row

        for (var col = 0; col < tableSize; col++) {

            var td = document.createElement("td");
            td.setAttribute("id", col + "," + row);  // set name
            td.setAttribute("class", "selectionSquare");

            td.style.width = ((100 / tableSize) / 2) + "%";
            td.style.height = (100 / tableSize) + "%";

            td.appendChild(document.createTextNode("\u0020"))  // add empty text

            tr.appendChild(td)  // append cell to row

        }

        tbdy.appendChild(tr);  // append row to table

    }

    tbl.appendChild(tbdy);  // add table to HTML
    body.appendChild(tbl);

}