var wallColour = "#F44336";
var foodColour = "#4CAF50";
var youColor = "#E91E63";
var snakeColours = ["#9C27B0", "#3F51B5", "#03A9F4", "#009688", "#CDDC39", "#FFEB3B", "#FF9800", "#FF5722", "#795548", "#607D8B"];


function main(){

  var width = window.innerWidth;
  var height = window.innerHeight;
  var boundary = 0;
  if(width < height){
    boundary = width;
  }else{
    boundary = height;
  }

  tableCreate(20, boundary);

  //var table = document.getElementById("table");
}


function cellClicked(elem){

  //console.log(elem.id);
  document.getElementById(elem.id).style.backgroundColor = snakeColours[Math.floor(Math.random() * snakeColours.length)];

}


function tableCreate(tableSize, windowSize) {

  var body = document.getElementsByTagName('body')[0];  // get body

  var tbl = document.createElement('table');  // declare table
  tbl.setAttribute('border', '1');
  tbl.setAttribute('id', 'table');
  tbl.style.width = (windowSize - 50) + 'px';
  tbl.style.height = (windowSize - 50) + 'px';

  var tbdy = document.createElement('tbody');  // declare body

  var cellSize = (100 / tableSize) + '%';  // declare cell size

  for (var row = 0; row < tableSize; row++) {  // for table size

    var tr = document.createElement('tr');  // declare row

    for (var col = 0; col < tableSize; col++) {

      var td = document.createElement('td');
      td.setAttribute('id', row + ',' + col);  // set name
      td.setAttribute('onclick', 'cellClicked(this)');  // make clickable
      td.style.width = cellSize;
      td.style.height = cellSize;

      td.appendChild(document.createTextNode('\u0020'))  // add empty text

      tr.appendChild(td)  // append cell to row

    }

    tbdy.appendChild(tr);  // append row to table

  }

  tbl.appendChild(tbdy);  // add table to HTML
  body.appendChild(tbl);

}
