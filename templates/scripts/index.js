
//function listens for page content to finish loading
document.addEventListener('DOMContentLoaded', function () {

    //gets all modals in account.html and initializes them so necessary event handlers and functions work
    var modals = document.querySelectorAll('.modal');
    M.Modal.init(modals);

});