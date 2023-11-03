$(document).ready (function () {
    getBookigs();
    
});

// AJAX call to retireve the list of bookings
function getBookigs(ajaxurl) {
    $.ajax({
        method: 'GET',
        url: "/partyup/view_bookings",
        success: function(data){  },
        error: function(req, err){ }
    })
}


