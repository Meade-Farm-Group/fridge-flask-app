
function loading(){
    $("#loader").removeClass("visually-hidden");
    $("#hideContent").hide();       
}
if(performance.navigation.type == 2){
    location.reload(true);
}