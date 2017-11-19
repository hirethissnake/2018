var snakeColours = ["#4CAF50","#607D8B","#E91E63","#9C27B0", "#3F51B5", "#03A9F4", "#009688", "#CDDC39", "#FFEB3B", "#FF9800", "#FF5722", "#795548"];
var snakesHead = [false, true, true, true, true, true, true, true, true, true, true, true, true];

var currentSelected = 0;
var tableSize = 20;
var mouseDown = 0;  // store mouse status
var width = 0;
var height = 0;
var tableWidth = 0;
var tableHeight = 0;
var turnCounter = 0;
var interID;
var paused = false;

var oneTurnData = {
    'you':'you',
    'turn':1,
    'snakes':[
        {'taunt':'gotta go slow',
        'name':'snake1',
        'id':'1',
        'health_points':100,
        'coords':[[7,2],[7,3],[7,4],[7,5],[7,6],[8,6]]},
        {'taunt':'gotta go slow',
        'name':'snake4',
        'id':'4',
        'health_points':100,
        'coords':[[4,11],[5,11],[6,11],[7,11],[7,12],[7,13],[8,13],[8,14],[8,15],[9,15]]},
        {'taunt':'gotta go slow',
        'name':'snake5',
        'id':'5',
        'health_points':100,
        'coords':[[16,13],[12,9],[13,9],[14,9],[15,9],[16,9],[12,10],[16,10],[12,11],[13,11],[13,12],[14,12],[15,13]]}
    ],
    'height':20,
    'width':20,
    'game_id':'gameid',
    'food':[
        [14,2],
        [3,6],
        [18,11],
        [12,13],
        [3,16]
    ],
    'dead_snakes':[]
};
var multiTurnData = [
    {"you":"you","turn":1,"snakes":[{"taunt":"gotta go fast","name":"sneakysnake","id":"you","health_points":100,"coords":[]},{"taunt":"gotta go slow","name":"snake0","id":"0","health_points":100,"coords":[[15,1],[15,2],[15,3],[15,4],[15,5],[15,6],[13,7],[14,7],[15,7],[13,8]]},{"taunt":"gotta go slow","name":"snake3","id":"3","health_points":100,"coords":[[7,17],[8,17],[9,17],[10,17],[11,17],[12,17],[13,17],[14,17],[14,18],[15,18]]}],"height":20,"width":20,"game_id":"gameid","food":[[4,2],[10,5],[17,8],[3,13],[16,15]],"dead_snakes":[]},
    {"you":"you","turn":1,"snakes":[{"taunt":"gotta go fast","name":"sneakysnake","id":"you","health_points":100,"coords":[]},{"taunt":"gotta go slow","name":"snake0","id":"0","health_points":100,"coords":[[14,1],[15,1],[15,2],[15,3],[15,4],[15,5],[15,6],[13,7],[14,7],[15,7]]},{"taunt":"gotta go slow","name":"snake3","id":"3","health_points":100,"coords":[[7,16],[7,17],[8,17],[9,17],[10,17],[11,17],[12,17],[13,17],[14,17],[14,18]]}],"height":20,"width":20,"game_id":"gameid","food":[[4,2],[10,5],[17,8],[3,13],[16,15]],"dead_snakes":[]},
    {"you":"you","turn":1,"snakes":[{"taunt":"gotta go fast","name":"sneakysnake","id":"you","health_points":100,"coords":[]},{"taunt":"gotta go slow","name":"snake0","id":"0","health_points":100,"coords":[[13,1],[14,1],[15,1],[15,2],[15,3],[15,4],[15,5],[15,6],[14,7],[15,7]]},{"taunt":"gotta go slow","name":"snake3","id":"3","health_points":100,"coords":[[7,15],[7,16],[7,17],[8,17],[9,17],[10,17],[11,17],[12,17],[13,17],[14,17]]}],"height":20,"width":20,"game_id":"gameid","food":[[4,2],[10,5],[17,8],[3,13],[16,15]],"dead_snakes":[]},
    {"you":"you","turn":1,"snakes":[{"taunt":"gotta go fast","name":"sneakysnake","id":"you","health_points":100,"coords":[]},{"taunt":"gotta go slow","name":"snake0","id":"0","health_points":100,"coords":[[12,1],[13,1],[14,1],[15,1],[15,2],[15,3],[15,4],[15,5],[15,6],[15,7]]},{"taunt":"gotta go slow","name":"snake3","id":"3","health_points":100,"coords":[[6,15],[7,15],[7,16],[7,17],[8,17],[9,17],[10,17],[11,17],[12,17],[13,17]]}],"height":20,"width":20,"game_id":"gameid","food":[[4,2],[10,5],[17,8],[3,13],[16,15]],"dead_snakes":[]}
];

var openFile = function(event) {
    var input = event.target;

    var reader = new FileReader();
    reader.onload = function(){
        var text = reader.result;
        oneTurnData = JSON.parse(text);

    };
    reader.readAsText(input.files[0]);
};

function main() {
    
    width = window.innerWidth - 50;
    height = window.innerHeight - 50;

    tableCreate();
}

function start() {
    interID = setInterval(newTurn, 1500);
    console.log(oneTurnData.length);
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

function newTurn() {
    console.log("Woahboi "+turnCounter);

    var thisTurn = oneTurnData[turnCounter];

    //Compare last turn to current turn to remove unused cells
    if (turnCounter > 0) {
        var lastTurn = oneTurnData[turnCounter-1];

        // Check if old food still exists
        for (x in lastTurn.food) {
            var oldKibbles = lastTurn.food[x];
            var oldFound = false;
            
            for (k in thisTurn.food) {
                if (oldKibbles == thisTurn.food[k]){oldFound=true; break;}
            }
            // if oldKibbles no longer exists, remove its color
            if (!oldFound) {
                document.getElementById(oldKibbles[0]+','+oldKibbles[1]).style.backgroundColor = null;
            }
        }

        // Check if old Snakes & their coords still exist
        for (x in lastTurn.snakes) {
            var oldSnake = lastTurn.snakes[x];
            var oldSnakeFound = false;

            // Check for this snakes existence
            for (k in thisTurn.snakes) {
                if (oldSnake.id == thisTurn.snakes[k].id) {
                    
                    // Check if the old coordinates still exist
                    for (j in oldSnake.coords) {
                        var oldCoord = oldSnake.coords[j];
                        var oldCorFound = false;

                        // Check for this coordinate's existence
                        for (f in thisTurn.snakes[k].coords) {
                            if (oldCoord == thisTurn.snakes[k].coords[f]){oldCorFound=true; break;}
                        }
                        // If coordinate was not found in new coords, remove its color
                        if (!oldCorFound) {
                            document.getElementById(oldSnake.coords[j][0]+','+oldSnake.coords[j][1]).style.backgroundColor = null;
                        }
                    }

                    oldSnakeFound=true;
                    break;
                }
            }
            // If snake was not found in new snakes, remove all of its color
            if (!oldSnakeFound) {
                for (j in oldSnake.coords) {
                    document.getElementById(oldSnake.coords[j][0]+','+oldSnake.coords[j][1]).style.backgroundColor = null;
                }
            }
        }
    }

    //Add data from new turn
    for (x in thisTurn.food){
        var kibbles = thisTurn.food[x];
        document.getElementById(kibbles[0]+','+kibbles[1]).style.backgroundColor = "rgb(76, 175, 80)";
    }
    for (x in thisTurn.snakes){
        var curSnake = thisTurn.snakes[x];
        for (k in curSnake.coords){
            var curCoord = curSnake.coords[k];
            console.log(curCoord);
            document.getElementById(curCoord[0]+','+curCoord[1]).style.backgroundColor = snakeColours[curSnake.id];
        }
    }

    turnCounter++;
    if (turnCounter >= oneTurnData.length) {
        clearInterval(interID);
    }
}