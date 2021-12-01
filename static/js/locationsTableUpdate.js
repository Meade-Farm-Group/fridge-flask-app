function getData(loc){
    $.ajax({
        url: '/update_data/'+loc,
        type: 'POST',
        success: function(data) {
            var table = document.getElementById("myTable");
            for (var i = 1, row; row = table.rows[i]; i++) {
                for (var j = 1, col; col = row.cells[j]; j++) {
                    cellUpdate(col, data);                    
                }
            }
        }
    });
}

function getData3d(loc){
    var rack = document.getElementById("rack_select").value;
    $.ajax({
        url: '/update_data/'+loc+"-"+rack,
        type: 'POST',
        success: function(data) {
            var table = document.getElementById("myTable");
            for (var i = 1, row; row = table.rows[i]; i++) {
                for (var j = 1, col; col = row.cells[j]; j++) {
                    cellUpdate(col, data);
                }
            }
        }
    });
}

function rackChange(loc, id){
    var rack = document.getElementById("rack_select").value;
    $.ajax({
        url: '/update_data/'+loc+"-"+rack,
        type: 'POST',
        success: function(data) {
            var table = document.getElementById("myTable");
            for (var i = 1, row; row = table.rows[i]; i++) {
                for (var j = 1, col; col = row.cells[j]; j++) {
                    //cellUpdate(col, data);                    
                }
            }
        }
    });
}

function replaceCellId(col, data, rack, i, j) {
    var cell = document.getElementById(col.id) //Cell Html object
    var cell_id = cell.getAttribute("cell-id"); // Getting the Id of the cell
    var col_link = col.getElementsByClassName("cell-link")[0]; 
    var newId = data["loc_id"] +"-"+ cell_id;
    col_link.innerHTML = "<div> Cell " + rack +"-"+ cell_id+"</div>";
    col_link.href="/palletInfo/"+newId;
    cell.setAttribute("id", newId);
}

function cellUpdate(col, data) {
    var col_link = col.getElementsByClassName("cell-link")[0];
    if (data["pallets"].includes(col.id)) {
        // Check to see if pallet cell is red. If yes, change it. If no, do nothing
        if (col.classList.contains("table-danger")) {
            col.classList.remove("table-danger");
            col.classList.add("table-success");
            col.classList.add("table-hover");
            col_link.classList.remove("class", "disabled");
        }
    }
    // if pallet does not exist
    else {
        // Check to see if cell is green. If yes, change it, if no, 
        if (col.classList.contains("table-success")) {
            col.classList.remove("table-success");
            col.classList.add("table-danger");
            col.classList.remove("table-hover");
            col_link.classList.add("class", "disabled");
        }
    }
}

//function tableLabelUpdate(rack):
