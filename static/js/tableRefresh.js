// function to refresh the table(s)
// it runs the getdata() initilly, then set the interval to run the function again every 1 minute using ajax
$(document).ready(function () {
    getData();
    setInterval(function () {
        getData();
    }, 60000);
});