$(document).ready(function () {
    var locData = $('#my-data').data();
    updatedTime = document.getElementById("updatedTime");

    updatedTime.innerHTML = '<div id="updateTime">' + formatDate(new Date()) + '</div>'
    getData(locData["loc"], locData["rack"]);
    setInterval(function () {
        getData(locData["loc"], locData["rack"]);
        updatedTime.innerHTML = '<div id="updateTime">' + formatDate(new Date()) + '</div>'
    }, 60000);
});

function formatDate(date) {
    var hours = date.getHours();
    var minutes = date.getMinutes();
    var ampm = hours >= 12 ? 'pm' : 'am';
    hours = hours % 12;
    hours = hours ? hours : 12; // the hour '0' should be '12'
    minutes = minutes < 10 ? '0'+minutes : minutes;
    var strTime = hours + ':' + minutes + ' ' + ampm;
    return strTime + "   " + date.getDate() + "/" + (date.getMonth()+1) + "/" + date.getFullYear();
}