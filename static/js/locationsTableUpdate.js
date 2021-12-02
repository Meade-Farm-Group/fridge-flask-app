function getData(loc, rack){
    var search = "";
    // If the rack value is "00", this means it is a 2d view of the storage
    // 2d storages do not have a rack value, so it defaults to 0, which is then
    // formatted to the desired digit length
    if (rack == 00){
        search = loc;
    }else{
        search = loc+"-"+rack;
    }
    $.ajax({
        url: '/update_data/'+search,
        type: 'POST',
        success: function(data) {
            var table = document.getElementById("palletTable");
            for (var i = 1, row; row = table.rows[i]; i++) {
                for (var j = 1, col; col = row.cells[j]; j++) {
                    cellUpdate(col, data);
                }
            }
        }
    });
}

function cellUpdate(col, data) {
    var col_link = col.getElementsByClassName("cell-link")[0];
    // If pallet exists in the list
    if (data["pallets"].includes(col.id)) {
        // Check to see if pallet cell is red. If yes, change it. If no, do nothing
        if (col.classList.contains("table-danger")) {
            col.classList.remove("table-danger");
            col.classList.add("table-success");
            col.classList.add("table-hover");
            col_link.classList.remove("class", "disabled");
        }
    }
    // if pallet does not exist in the list
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

function goBack() {
    window.history.back();
}

