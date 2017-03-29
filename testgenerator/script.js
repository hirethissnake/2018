var snakeColours = ["#4CAF50","#607D8B","#E91E63","#9C27B0", "#3F51B5", "#03A9F4", "#009688", "#CDDC39", "#FFEB3B", "#FF9800", "#FF5722", "#795548"];
var snakesHead = [false, true, true, true, true, true, true, true, true, true, true, true, true];

var currentSelected = 0;
var tableSize = 20;
var mouseDown = 0;  // store mouse status
var width = 0;
var height = 0;
var tableWidth = 0;
var tableHeight = 0;

function main(){

  width = window.innerWidth - 50;
  height = window.innerHeight - 50;

  mouseClick();
  tableCreate();
  addColumns();
  fillSelector();
  fillTools();

}


function mouseClick(){

  document.body.setAttribute("onmousedown", "mouseDown = 1");
  document.body.setAttribute("onmouseup", "mouseDown = 0");

}


function cellClicked(elem){

  var cell = document.getElementById(elem.id);
  if(cell.class != currentSelected){
    cell.innerHTML = "";
    if(cell.innerHTML == "h"){
      snakesHead[cell.className] = true;
    }if(cell.innerHTML == "t"){
      snakesTail[cell.className] = true;
    }
  }
  cell.style.backgroundColor = snakeColours[currentSelected];
  cell.className = currentSelected;
  if(currentSelected != 0){
    if(snakesHead[currentSelected]){
      cell.innerHTML = "h";
      snakesHead[currentSelected] = false;
    }else{
      var cells = document.getElementsByClassName(currentSelected);
      for(var tempCell of cells){
        if(tempCell.innerHTML != "h"){
          tempCell.innerHTML = "";
        }
      }
      cell.innerHTML = "t";
    }
  }

}


function cellHover(elem){

  if(mouseDown == 1){
    cellClicked(elem);
  }

}


function selected(elem){

  var currentId = elem.id.split("colour")[1];
  for(var i = 0; i < 12; i++){
    document.getElementById("colour" + i).childNodes[0].childNodes[0].setAttribute("border", "0");
  }
  if(currentSelected != currentId){
    elem.style.fontWeight = "bold";
    elem.childNodes[0].childNodes[0].setAttribute("border", "3");
    var deBold = document.getElementById("colour" + currentSelected).style.fontWeight = "normal";  // get current bold
    currentSelected = currentId;  // store selected
  }

}


function hover(elem){

  var tableSwatch = elem.childNodes[0].childNodes[0];
  tableSwatch.setAttribute("border", "3");

}


function dehover(elem){

  if(elem.id.split("colour")[1] != currentSelected){
    var tableSwatch = elem.childNodes[0].childNodes[0];
    tableSwatch.setAttribute("border", "0");
  }

}


function tableCreate() {

  var body = document.getElementsByTagName("body")[0];  // get body

  var tbl = document.createElement("table");  // declare table
  tbl.setAttribute("border", "1");
  tbl.setAttribute("id", "table");

  if(width > height){
    var desiredWidth = width;
    if(height < width / 2){
      tableWidth = tbl.style.width = (height * 2);
      tableHeight = tbl.style.height = height;
    }else{
      tableWidth = tbl.style.width = width;
      tableHeight = tbl.style.height = (width / 2);
    }
  }

  var tbdy = document.createElement("tbody");  // declare body

  for (var row = 0; row < tableSize; row++) {  // for table size

    var tr = document.createElement("tr");  // declare row

    for (var col = 0; col < tableSize; col++) {

      var td = document.createElement("td");
      td.setAttribute("id", row + "," + col);  // set name
      td.setAttribute("class", "selectionSquare");

      td.setAttribute("onclick", "cellClicked(this)");  // make clickable
      td.setAttribute("onmouseover", "cellHover(this)");  // enable drag select
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


function addColumns() {

  var tbl = document.getElementById("table");
  var cell = tbl.rows[0].insertCell(tbl.rows[0].cells.length);  // create cell

  cell.setAttribute("id", "selector");
  cell.setAttribute("rowspan", tableSize);  // spans entire height
  cell.setAttribute("width", (tableWidth / 4) + "px");  // half table width

  cell.appendChild(document.createTextNode("\u0020"));  // add to table

  var cell = tbl.rows[0].insertCell(tbl.rows[0].cells.length);  // create cell

  cell.setAttribute("id", "tools");
  cell.setAttribute("rowspan", tableSize);  // spans entire height
  cell.setAttribute("width", (tableWidth / 4) + "px")  // half table width

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

  for (var row = 0; row < snakeColours.length; row++) {  // for each colour

    var tr = document.createElement("tr");  // declare row
    tr.setAttribute("id", "colour" + row);  // make referenceable
    if(row == 0){
      tr.style.fontWeight = "bold";
    }
    tr.setAttribute("onClick", "selected(this)");  // when clicked
    tr.setAttribute("onmouseover", "hover(this)");  // bold on hover
    tr.setAttribute("onmouseout", "dehover(this)");

    for (var col = 0; col < 2; col++) { // 2 columns

      var td = document.createElement("td");

      td.setAttribute("align", "center");

      if(col == 0){

        var innertbl = document.createElement("table");  // declare table
        td.style.width = "30%";

        innertbl.setAttribute("border", "0");
        innertbl.style.width = "70%";
        innertbl.style.height = "90%";

        var innertbdy = document.createElement("tbody");  // declare body
        var innertr = document.createElement("tr");  // declare row
        var innertd = document.createElement("td");

        innertd.style.backgroundColor = snakeColours[row];  // set colour swatch

        innertr.appendChild(innertd);
        innertbdy.appendChild(innertr);
        innertbl.appendChild(innertbdy)

        td.appendChild(innertbl)  // add empty text

      }else{

        td.style.width = "70%";

        var p;
        if(row == 0){
          p = document.createTextNode("Food");
        }else if(row == 1){
          p = document.createTextNode("You");
        }else{
          p = document.createTextNode("Snake " + (row - 2));
        }

        td.style.textAlign = "left";
        td.appendChild(p);  // add label

      }

      td.style.height = (tableHeight / snakeColours.length) + "px";

      tr.appendChild(td)  // append cell to row

    }

    tbdy.appendChild(tr);  // append row to table

  }

  tbl.appendChild(tbdy);  // add table to HTML
  selector.appendChild(tbl);

  document.getElementById("colour0").childNodes[0].childNodes[0].setAttribute("border", "3");

}


function fillTools(){

  var selector = document.getElementById("tools");

  var tbl = document.createElement("table");  // declare table
  tbl.setAttribute("border", "0");
  tbl.setAttribute("id", "toolsTable");
  tbl.style.width = "100%";
  tbl.style.height = "100%";

  var tbdy = document.createElement("tbody");  // declare body

  var numTools = 3;

  var tr = document.createElement("tr");  // declare row

  var button = document.createElement("button");
  button.innerHTML = "Clear Table";
  button.style.height = (tableHeight / numTools)  - 10 + "px";
  button.style.width = (tableWidth / 8) + "px";
  button.style.marginTop = "10px";

  var body = document.getElementsByTagName("body")[0];
  tr.appendChild(button);
  button.parentElement.setAttribute("align", "center");

  button.addEventListener ("click", function() {
    clearTable();
  });

  tbdy.appendChild(tr);  // append row to table

  tr = document.createElement("tr");  // declare row

  var button = document.createElement("button");
  button.innerHTML = "Move Head";
  button.style.height = (tableHeight / numTools)  - 10 + "px";
  button.style.width = (tableWidth / 8) + "px";
  button.style.marginTop = "10px";

  var body = document.getElementsByTagName("body")[0];
  tr.appendChild(button);
  button.parentElement.setAttribute("align", "center");

  button.addEventListener ("click", function() {
    moveHead();
  });

  tbdy.appendChild(tr);  // append row to table

  tr = document.createElement("tr");  // declare row

  var button = document.createElement("button");
  button.innerHTML = "Erase";
  button.style.height = (tableHeight / numTools)  - 10 + "px";
  button.style.width = (tableWidth / 8) + "px";
  button.style.marginTop = "10px";

  var body = document.getElementsByTagName("body")[0];
  tr.appendChild(button);
  button.parentElement.setAttribute("align", "center");

  button.addEventListener ("click", function() {
    erase();
  });

  tbdy.appendChild(tr);  // append row to table

  tbl.appendChild(tbdy);  // add table to HTML
  selector.appendChild(tbl);

}


function clearTable(){

  for (var row = 0; row < tableSize; row++) {  // for table size

    var tr = document.createElement("tr");  // declare row

    for (var col = 0; col < tableSize; col++) {

      var td = document.getElementById(row + "," + col);  // get by name
      td.style.backgroundColor = "#FFFFFF";
      td.class = "";
      td.innerHTML = "";
      snakesHead = [false, true, true, true, true, true, true, true, true, true, true, true, true];

    }

  }

}

function moveHead(){

  var cells = document.getElementsByClassName(currentSelected);
  for(var cell of cells){
    if(cell.innerHTML == "h"){
      cell.innerHTML = "";
    }
  }
  if(currentSelected != 0){
    snakesHead[currentSelected] = true;
  }

}

function erase(){

  currentSelected = -1; // currently breaks functions

}
