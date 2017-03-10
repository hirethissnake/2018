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
  appendColumn();

  //var table = document.getElementById("table");
}


function cellClicked(elem){

  //console.log(elem.id);
  document.getElementById(elem.id).style.backgroundColor = snakeColours[Math.floor(Math.random() * snakeColours.length)];

}


function tableCreate(tableSize) {

  var body = document.getElementsByTagName('body')[0];  // get body

  var tbl = document.createElement('table');  // declare table
  tbl.setAttribute('border', '1');
  tbl.setAttribute('id', 'table');
  tbl.style.width = (2 * (windowSize - 50)) + 'px';
  tbl.style.height = (windowSize - 50) + 'px';

  var tbdy = document.createElement('tbody');  // declare body

  for (var row = 0; row < tableSize; row++) {  // for table size

    var tr = document.createElement('tr');  // declare row

    for (var col = 0; col < tableSize; col++) {

      var td = document.createElement('td');
      td.setAttribute('id', row + ',' + col);  // set name
      td.setAttribute('onclick', 'cellClicked(this)');  // make clickable
      td.style.width = ((100 / tableSize) / 2) + "%";
      td.style.height = (100 / tableSize) + "%";

      td.appendChild(document.createTextNode('\u0020'))  // add empty text

      tr.appendChild(td)  // append cell to row

    }

    tbdy.appendChild(tr);  // append row to table

  }

  tbl.appendChild(tbdy);  // add table to HTML
  body.appendChild(tbl);

}

function createCell(cell) {

  var div = document.createElement('div'); // create DIV element
  div.appendChild(document.createTextNode('\u0020'));  // append text node to the DIV
  cell.setAttribute('rowspan', 20);
  div.style.width = (windowSize / 2) + "px";
  cell.appendChild(div);                   // append DIV to the table cell

}

function appendColumn() {
  var tbl = document.getElementById('table'), // table reference
  // open loop for each row and append cell
  i;
  for (i = 0; i < tbl.rows.length; i++) {
    if(i==0){createCell(tbl.rows[i].insertCell(tbl.rows[i].cells.length));}
  }
}
