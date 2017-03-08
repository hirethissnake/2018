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

  console.log(table);


}

function cellClicked(elem){
  console.log(elem.id);
}

function tableCreate(tableSize, windowSize) {
  var body = document.getElementsByTagName('body')[0];
  var tbl = document.createElement('table');
  var cellSize = (100 / tableSize) + '%';
  console.log(windowSize);
  tbl.style.width = (windowSize - 50) + 'px';
  tbl.style.height = (windowSize - 50) + 'px';
  tbl.setAttribute('border', '1');
  tbl.setAttribute('id', 'table');
  var tbdy = document.createElement('tbody');
  for (var row = 0; row < tableSize; row++) {
    var tr = document.createElement('tr');
    for (var col = 0; col < tableSize; col++) {
      var td = document.createElement('td');
      td.setAttribute('id', row + ',' + col);
      td.style.width = cellSize;
      td.style.height = cellSize;
      td.setAttribute('onclick', 'cellClicked(this)');
      td.appendChild(document.createTextNode('\u0020'))
      tr.appendChild(td)
    }
    tbdy.appendChild(tr);
  }
  tbl.appendChild(tbdy);
  body.appendChild(tbl)
}
