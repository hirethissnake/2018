var wallColour = "#F44336";
var foodColour = "#4CAF50";
var youColor = "#E91E63";
var snakeColours = ["#9C27B0", "#3F51B5", "#03A9F4", "#009688", "#CDDC39", "#FFEB3B", "#FF9800", "#FF5722", "#795548", "#607D8B"];

var windowSize = 0;

function main(){

  var width = window.innerWidth;
  var height = window.innerHeight;
  if(width < height){
    windowSize = width - 100;
  }else{
    windowSize = height - 100;
  }

  tableCreate(20);
  addSelector();
  fillSelector();

  //var table = document.getElementById("table");
}


function cellClicked(elem){

  //console.log(elem.id);
  document.getElementById(elem.id).style.backgroundColor = snakeColours[Math.floor(Math.random() * snakeColours.length)];

}


function tableCreate(tableSize) {

  var body = document.getElementsByTagName("body")[0];  // get body

  var tbl = document.createElement("table");  // declare table
  tbl.setAttribute("border", "1");
  tbl.setAttribute("id", "table");
  tbl.style.width = (2 * (windowSize - 50)) + "px";
  tbl.style.height = (windowSize - 50) + "px";

  var tbdy = document.createElement("tbody");  // declare body

  for (var row = 0; row < tableSize; row++) {  // for table size

    var tr = document.createElement("tr");  // declare row

    for (var col = 0; col < tableSize; col++) {

      var td = document.createElement("td");
      td.setAttribute("id", row + "," + col);  // set name
      td.setAttribute("onclick", "cellClicked(this)");  // make clickable
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


function addSelector() {

  var tbl = document.getElementById("table");
  var cell = tbl.rows[0].insertCell(tbl.rows[0].cells.length);  // create cell

  cell.setAttribute("id", "selector");
  cell.setAttribute("rowspan", 20);  // spans entire height
  cell.style.width = (windowSize / 2) + "px";  // half table width

  cell.appendChild(document.createTextNode("\u0020"));  // add to table

}


function fillSelector(){

  var selector = document.getElementById("selector");

  var tbl = document.createElement("table");  // declare table
  tbl.setAttribute("border", "0");
  tbl.setAttribute("id", "selectorTable");
  tbl.style.width = "100%";
  tbl.style.height = "100%";

  var tbdy = document.createElement("tbody");  // declare body

  for (var row = 0; row < 3; row++) {  // for table size

    var tr = document.createElement("tr");  // declare row

    for (var col = 0; col < 2; col++) {

      var td = document.createElement("td");
      td.setAttribute("id", row + "," + col);  // set name
      td.setAttribute("align", "center");
      td.style.width = "50%";
      td.style.height = "33%";

      var innertbl = document.createElement("table");  // declare table
      innertbl.setAttribute("border", "0");
      innertbl.style.width = "25%";
      innertbl.style.height = "25%";

      var innertbdy = document.createElement("tbody");  // declare body
      var innertr = document.createElement("tr");  // declare row
      var innertd = document.createElement("td");
      innertr.appendChild(innertd);
      innertbdy.appendChild(innertr);
      innertbl.appendChild(innertbdy)

      td.appendChild(innertbl)  // add empty text

      tr.appendChild(td)  // append cell to row

    }

    tbdy.appendChild(tr);  // append row to table

  }

  tbl.appendChild(tbdy);  // add table to HTML
  selector.appendChild(tbl);

  // p.innerHTML = "temp test";
  // selector.appendChild(p);

}
