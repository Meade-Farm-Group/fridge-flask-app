function getData(loc, rack) {
    var search = "";
    // If the rack value is "00", this means it is a 2d view of the storage
    // 2d storages do not have a rack value, so it defaults to 0, which is then
    // formatted to the desired digit length
    if (rack == 00) {
        search = loc;
    } else {
        search = loc + "-" + rack;
    }
    $.ajax({
        url: '/update_data/' + search,
        type: 'POST',
        success: function (data) {
            var table = document.getElementById("cellTable");
            $.getJSON("/static/js/mascodeColours.json", function (masCodeColours) {
                legendList = {};
                
                for (var i = 1, row; row = table.rows[i]; i++) {
                    for (var j = 1, col; col = row.cells[j]; j++) {
                        legendList = cellUpdate(col, data, masCodeColours, legendList);
                    }
                }
                // Update the legend
                updateLegend(masCodeColours, legendList);
            });
        }
    });
    // showUpdateMsg();
}
function cellUpdate(col, data, masCodeColours, legendList) {
    var col_link = col.getElementsByClassName("cell-link")[0];
    var masCode;
    var bgColour;
    // If cell id exists in the list
    if (col.id in data["pallets"]) {
        col.classList.add("table-hover");
        col_link.classList.remove("class", "disabled");

        // Check to see if the array are all the same value
        if (data["pallets"][col.id].every((val, i, arr) => val === arr[0])) {
            // Gets the colour of the cell based on what master code it is
            // from a json file that was called and passed into this function
            masCode = data["pallets"][col.id][0]
            bgColour = masCodeColours[masCode]
            if (typeof bgColour === 'undefined') {
                bgColour = "#000000"
            }

            $(col).css("background-color", bgColour);
            cellText = col.getElementsByTagName("Div")[0]
            if(checkBrightness(bgColour)){
                $(cellText).css("color", "white");
            }else{
                $(cellText).css("color", "black");
            }
        }
        else { // If all values are not the same, we will display it a colour to represent mixed
            masCode = "MIXD";
            $(col).css("background-color", masCodeColours[masCode]);
        }

        // Array containing all mascodes and colours that is currently being displayed
        // on the table
        if (!(masCode in legendList)){
            legendList[masCode] = data["masCodeNames"][masCode];
        }

    }
    // if cell id does not exist in the list
    else {
        // Check to see if cell is green. If yes, change it, if no,
        $(col).css("background-color", "white");
        col.classList.remove("table-hover");
        col_link.classList.add("class", "disabled");
    }
    return legendList;
}

function updateLegend(masCodeColours, legendList){
    $("#testDisplay div").remove(); 
    var name;
    for (var key in legendList) {
        if (legendList.hasOwnProperty(key)) {

            bgColour = masCodeColours[key];
            var element = document.createElement("div");
            element.classList.add("col-md");
            element.classList.add("legendSample");
            element.classList.add("text-center");
            $(element).css("background-color", bgColour);
            
            if(checkBrightness(bgColour)){
                $(element).css("color", "white");
            }

            if (typeof legendList[key] === 'undefined') {
                name = 'Mixed'
            }else{
                name = legendList[key];
            }

            element.innerHTML = name;
            document.getElementById('testDisplay').appendChild(element); 
        }
    }
}

function showUpdateMsg() {
    $("#success-alert").fadeTo(2000, 500).slideUp(500, function () {
        $("#success-alert").slideUp(500);
    });
}

function checkBrightness(bgColour){
    var bgColour = bgColour.substring(1);      // strip #
    var rgb = parseInt(bgColour, 16);   // convert rrggbb to decimal
    var r = (rgb >> 16) & 0xff;  // extract red
    var g = (rgb >>  8) & 0xff;  // extract green
    var b = (rgb >>  0) & 0xff;  // extract blue

    var luma = 0.2126 * r + 0.7152 * g + 0.0722 * b; // per ITU-R BT.709
    if (luma < 115) {
        return true
    }else{
        return false
    }
}
