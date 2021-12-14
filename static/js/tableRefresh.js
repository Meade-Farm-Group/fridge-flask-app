$(document).ready(function () {
    getData();
    setInterval(function () {
        getData();
    }, 60000);
});