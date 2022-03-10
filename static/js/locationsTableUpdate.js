function getData() {     
    var search = "";
    var range;
    var locData = $('#my-data').data();
    // If the rack value is "00", this means it is a 2d view of the storage
    // 2d storages do not have a rack value, so it defaults to 0, which is then
    // formatted to the desired digit length
    if (locData["rack"] == 00) {
        search = locData["loc"];
        range = 2
    } else {
        search = locData["loc"] + "-" + locData["rack"];
        range = 1
    }
    $.ajax({
        url: '/update_data/' + search,
        type: 'POST',
        success: function (data) {
            var tableNum;
            var table;
            $.getJSON("/static/js/mascodeColours.json", function (masCodeColours) {
                legendList = {};
                for (var k = 1; k <= range ; k++) {
                    tableNum = "cellTable" + k;
                    table = document.getElementById(tableNum);
                    for (var i = 1, row; row = table.rows[i]; i++) {
                        for (var j = 1, col; col = row.cells[j]; j++) {
                            // Function returns the legend list so that it can be updated
                            legendList = cellUpdate(col, data, masCodeColours, legendList);
                        }
                    }
                }
                // Update the legend
                updateLegend(masCodeColours, legendList, range);
            });
        }
    });
    // Update the time of last update done
    updatedTime = document.getElementById("updatedTime");
    updatedTime.innerHTML = '<div id="updateTime">' + formatDate(new Date()) + '</div>'

    // showUpdateMsg();
}

// Function checks each cell to see if there are pallets within them
// It is provided the cell
function cellUpdate(cell, data, masCodeColours, legendList) {
    var cell_link = cell.getElementsByClassName("cell-link")[0];
    var masCode;
    var bgColour;
    var filter = $('#my-data').data();
    // If cell id exists in the list
    if (cell.id in data["pallets"]) {
        cell.classList.add("table-hover");
        cell_link.classList.remove("class", "disabled");

        // Check to see if the array are all the same value
        if (data["pallets"][cell.id].every((val, i, arr) => val === arr[0])) {
            // Gets the colour of the cell based on what master code it is
            // from a json file that was called and passed into this function
            masCode = data["pallets"][cell.id][0]
            // Get the colour using the provided master code
            bgColour = masCodeColours[masCode]
            // If the master code does not have a colour yet, give it a default colour
            if (bgColour == '') {
                bgColour = "#000000"
            }
        }
        else { 
            // If all values are not the same, we will display it a colour to represent mixed
            masCode = "MIXD";
            bgColour = masCodeColours[masCode]
        }
        // Set the background colour of the cell
        $(cell).css("background-color", bgColour);
        // Get the element that has the text
        cellText = cell.getElementsByTagName("Div")[0]

        // Check if the colour is dark
        if(checkBrightness(bgColour)){
            // If the colour is dark, make the text white
            $(cellText).css("color", "#FFFFFF");
        }else{
            // If the colour is light, keep text dark
            $(cellText).css("color", "#000000");
        }
        
        // Set this attribute of the cell to the master code given it
        cell.setAttribute("data-masCode", masCode);


        // Check if the product is in quarantine(needs to be checked)
        // if (isQuarantined == true){
        //     cell.classList.add("stripe");
        //     $(cellText).css("color", "#FFFFFF");
        // }
        //cell.classList.add("stripe");
        // cell.getElementsByTagName("div")[0].classList.add("stripe");
        // $(cellText).css("color", "#FFFFFF");
        

        // Array containing all mascodes and colours that is currently being displayed
        // on the table. Check to see if mastercode exists in the array
        if (!(masCode in legendList)){
            // If master code does not exist in the array, add it
            legendList[masCode] = data["masCodeNames"][masCode];
        }

    }
    // if cell id does not exist in the list
    else {
        // if cell id does not exist in the list, disable the cell
        $(cell).css("background-color", "#FFFFFF");
        cell.setAttribute("data-masCode","");
        cell.classList.remove("table-hover");
        cell_link.classList.add("class", "disabled");
    }

    // Check used if in the case a filter is on and a cell gets updated with new data
    // If the master code of this cell matches the current filter AND if the filter is not empty
    // (meaning there is a filter on)
    if(filter['currentfilter'] != masCode && filter['currentfilter'] != ""){
        cell.classList.add("darkenCell");
    }else{
        cell.classList.remove("darkenCell");
    }
    return legendList;
}

function updateLegend(masCodeColours, legendList, range){
    // clearing the legend table
    $("#legendDisplay button").remove();
    $("#legendDisplay div").remove();
    var name
    var counter = 0;
    var filter = $('#my-data').data();
    // loops for the amount of unique master codes
    for (var key in legendList) {
        if (legendList.hasOwnProperty(key)) {
            // Getting the colour associated with the master code
            bgColour = masCodeColours[key];
            // Creating a button element and giving it relevant design and functionality
            var element = document.createElement("button");
            element.classList.add("col");
            element.classList.add("legendSample");
            element.classList.add("text-center");
            element.setAttribute("id", key);
            element.setAttribute("onclick","toggleFilter('"+key+"','"+range+"');");
            $(element).css("background-color", bgColour);
            
            // check to see if the colour of the background is dark
            if(checkBrightness(bgColour)){
                // If the colour is considered dark, make the text on it white
                $(element).css("color", "#FFFFFF");
            }

            // If the key does not have a name, it must be mixed, as mixed is not defined as a master code 
            // in the database
            if (typeof legendList[key] === 'undefined') {
                name = 'Mixed'
            }else{
                name = legendList[key];
            }

            // Check used if in the case a filter is on and a cell gets updated with new data
            // If the master code of this cell matches the current filter AND if the filter is not empty
            // (meaning there is a filter on)
            if(filter['currentfilter'] != key && filter['currentfilter'] != ""){
                element.classList.add("darkenCell");
            }

            // Add the name to the button
            element.innerHTML = name;
            // Add the button to the legend div
            document.getElementById('legendDisplay').appendChild(element);
            counter++;
        }
    }
    // If the location has no pallets, the coutner in the loop wll remian 0
    // In this case, a message will be displayed to indicate this.
    if (counter == 0){
        var element = document.createElement("div");
        element.classList.add("text-center");
        element.innerHTML = "<h3>No pallets found.</h3>";
        document.getElementById('legendDisplay').appendChild(element); 
    }
}

// Function to allow for all cells that arent the one selected in the reference
// to be darkened, or if the same legend option is selected, remove darkened class
function toggleFilter(key, range){
    // get data saved to html
    var filter = $('#my-data').data();
    // To check each cell, looping through the cell is necessary
    for (var k = 1; k <= range ; k++) {
        tableNum = "cellTable" + k;
        table = document.getElementById(tableNum);
        for (var i = 1, row; row = table.rows[i]; i++) {
            for (var j = 1, col; col = row.cells[j]; j++) {
                // if the key given is the same as the current filter, this means the user
                // is pressing the filter button again, thus turn off 
                if(key == filter['currentfilter']){
                    col.classList.remove("darkenCell")
                }else{
                    if (key != col.getAttribute("data-mascode")){
                        col.classList.add("darkenCell")
                    }else{
                        col.classList.remove("darkenCell")
                    }
                }    
            }
        }
    }
    // Applying css to buttons that werent pressed
    // Get the number of buttons in the display
    var legendDisplayLength = $("#legendDisplay button").length;
    // loop through each button element
    for (var i = 0; i <= legendDisplayLength-1 ; i++) {
        filterButton = document.getElementById("legendDisplay").getElementsByTagName("button")[i]
        // check if the filter is currently active
        if(key == filter['currentfilter']){
            // If the current filter is the same as the pressed filter, remove all filtering
            filterButton.classList.remove("darkenCell")
        }else{
            // if the filter id is not the master code that is being filtered
            if (filterButton.id != key ){
                filterButton.classList.add("darkenCell")
            }else{
                filterButton.classList.remove("darkenCell")
            }
        }
    }
    if(key == filter['currentfilter']){
        filter['currentfilter'] = "";
    }else{
        filter['currentfilter'] = key;
    }
}

function formatDate(date) {
    var hours = date.getHours();
    var minutes = date.getMinutes();
    var seconds = date.getSeconds();
    var ampm = hours >= 12 ? 'pm' : 'am';
    hours = hours % 12;
    hours = hours ? hours : 12; // the hour '0' should be '12'
    minutes = minutes < 10 ? '0'+minutes : minutes;
    seconds = seconds < 10 ? '0'+seconds : seconds;
    var strTime = hours + ':' + minutes +'.'+ seconds +' ' + ampm;
    return strTime + "   " + date.getDate() + "/" + (date.getMonth()+1) + "/" + date.getFullYear();
}

// Function to calculate how dark the colour is
function checkBrightness(bgColour){
    var bgColour = bgColour.substring(1);      // strip #
    var rgb = parseInt(bgColour, 16);   // convert rrggbb to decimal
    var r = (rgb >> 16) & 0xff;  // extract red
    var g = (rgb >>  8) & 0xff;  // extract green
    var b = (rgb >>  0) & 0xff;  // extract blue

    var luma = 0.2126 * r + 0.7152 * g + 0.0722 * b; // per ITU-R BT.709
    // if the colour is considered too dark, return true for editing of child elements within
    if (luma < 115) {
        return true
    }else{
        return false
    }
}