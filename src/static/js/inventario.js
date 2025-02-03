function capitalizeFirstLetter(string) {
    return string.charAt(0).toUpperCase() + string.slice(1).toLowerCase();
}
function init(){
  var estado=document.getElementById("status-container").getAttribute("data-estado");
  capitalizeFirstLetter(estado);
}
document.getElementById("DOMContentLoaded", init);