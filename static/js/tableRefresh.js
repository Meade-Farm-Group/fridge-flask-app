// function to refresh the table(s)
$(document).ready(function () {
    getData();
    setInterval(function () {
        getData();
    }, 60000);
});