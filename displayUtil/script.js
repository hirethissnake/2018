

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
      }else{
        tableWidth = tbl.style.width = width;
        tableHeight = tbl.style.height = (width / 2);
      }
    
      var tbody = document.createElement("tbody");  // declare body
    
      for (var row = 0; row < tableSize; row++) {  // for table size
    
        var tableRow = document.createElement("tr");  // declare row
    
        for (var col = 0; col < tableSize; col++) {
    
          var rowCell = document.createElement("rowCell");
          rowCell.setAttribute("id", col + "," + row);  // set name
          rowCell.setAttribute("class", "selectionSquare");
    
          rowCell.style.width = ((100 / tableSize) / 2) + "%";
          rowCell.style.height = (100 / tableSize) + "%";
    
          rowCell.appendChild(document.createTextNode("\u0020"))  // add empty text
    
          tableRow.appendChild(rowCell)  // append cell to row
    
        }
    
        tbody.appendChild(tableRow);  // append row to table
    
      }
    
      tbl.appendChild(tbody);  // add table to HTML
      body.appendChild(tbl);
    
    }