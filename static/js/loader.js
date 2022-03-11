
function loading(){
    $("#loader").removeClass("visually-hidden");
    $("#hideContent").hide();       
}
window.addEventListener("pageshow", function ( event ) {
    $("#loader").addClass("visually-hidden");
    $("#hideContent").show();
})
