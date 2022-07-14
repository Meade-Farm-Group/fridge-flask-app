// function to show and hide the loading icon
function loading(){
    // remove the class that is hiding the loader
    $("#loader").removeClass("visually-hidden");
    // hide all content that is wrapped in the div with id of 'hideContent'
    $("#hideContent").hide();       
}
// when the page loads
window.addEventListener("pageshow", function ( event ) {
    // hide the loader
    $("#loader").addClass("visually-hidden");
    // show the content
    $("#hideContent").show();
})
