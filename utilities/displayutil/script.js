const snakeColours = ["#607D8B","#E91E63","#9C27B0", "#3F51B5", "#03A9F4", "#009688", "#CDDC39", "#FFEB3B", "#FF9800", "#FF5722", "#795548"];
const snakeFaces = [":)", ":O", "xD", ":P", ">:(", "8)", ":C", ":3", ":E"]

const tableSize = 20;
let width = 0;
let height = 0;
let tableWidth = 0;
let tableHeight = 0;
let turnCounter = 0;
let interLength = 200;
let interID;
let paused = true;

var openFile = function(event) {
    const input = event.target;

    const reader = new FileReader()
    reader.onload = function(){
        const text = reader.result
        turnData = JSON.parse(text)
        let status = document.getElementById("status")

        for (member in turnData[0].snakes.data) {
            const name = turnData[0].snakes.data[member].name
            snakeStat = document.createElement("div")
            snakeStat.setAttribute("id", name)
            snakeStat.style.backgroundColor = snakeColours[member]

            pickedColor[name] = snakeColours[member]
            pickedFace[name] = snakeFaces[member]

            status.appendChild(snakeStat)
        }

        playTurn()
    };
    reader.readAsText(input.files[0]);
};

function main() {  
    width = window.innerWidth - 50;
    height = window.innerHeight - 50;

    snakeColours.sort(function() { return 0.5 - Math.random() });
    snakeFaces.sort(function() { return 0.5 - Math.random() });

    //tableCreate()
    createTable()
}

function start() {
    console.log(turnData.length)
    if (paused) {
        interID = setInterval(playTurn, interLength)
        paused = false
    } else {
        console.log("Already playing!")
    }
}

function playTurn() {
    turnCounter++
    if (turnCounter >= turnData.length-1) {
        console.log("Woahboi")
        pause()
    }
    clearCells()
    renderTurn(turnCounter)
    turnDisplay(turnCounter)
    displayHealth(turnCounter)
}

function pause() {
    clearInterval(interID)
    paused = true
}

function turnDisplay(curTurn) {
    document.getElementById('turnDisplay').innerText = "Current Turn: "+curTurn
}

function displayHealth(curTurn){
    for (member in turnData[curTurn].snakes.data) {
        const name = turnData[curTurn].snakes.data[member].name
        const health = turnData[curTurn].snakes.data[member].health
        document.getElementById(name).innerText = name+"\'s "+"health: "+health
    }
}
function jumpSubmit() {
    const jumpToTurn = document.getElementById('thisTurn').value;
    jumpTo(jumpToTurn)
}

function jumpTo(toHere) {
    if (1 <= toHere && toHere <= turnData.length) {
        console.log("Jumping to "+toHere)
        turnCounter = toHere
        clearCells()
        renderTurn(turnCounter)
        turnDisplay(turnCounter)
        displayHealth(turnCounter)
        if (turnCounter >= turnData.length) {
            pause()
        }
    }
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

function minusOne() {
    jumpTo(turnCounter-1)
}

function plusOne() {
    jumpTo(turnCounter+1)
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
    const curTurn = turnData[turnToRender-1]

    //Add food for new turn
    for (x in curTurn.food.data){
        const kibbles = curTurn.food.data[x]
        document.getElementById(kibbles['x']+','+kibbles['y']).style.backgroundColor = "rgb(76, 175, 80)"
    }
    //Add snakes for new turn
    for (x in curTurn.snakes.data){
        const curSnake = curTurn.snakes.data[x]
        for (k in curSnake.body.data){
            const curCoord = curSnake.body.data[k]
            document.getElementById(curCoord['x']+','+curCoord['y']).style.backgroundColor = pickedColor[curSnake.name]
            if (k == 0) {
                document.getElementById(curCoord['x']+','+curCoord['y']).innerText = pickedFace[curSnake.name]
            }
        }
    }
}

function createTable() {
    let table = document.getElementById("tableDiv")

    for (let row = 0; row < tableSize; row++) {
        let tableRow = document.createElement("div")
        tableRow.setAttribute("class", "boardRow")

        for (let col = 0; col < tableSize; col++) {
            let tableCell = document.createElement("div")
            tableCell.setAttribute("id", col+","+row)
            tableCell.setAttribute("class", "boardTile")

            tableRow.appendChild(tableCell)
        }
        table.appendChild(tableRow)
    }
}