$(document).ready (function () {
    getUserDetails();
    
});

// AJAX call to retireve the list of vendors
function getUserDetails(ajaxurl) {
    $.ajax({
        method: 'GET',
        url: "/partyup/vendor_list",
        success: function(data){ onSuccess },
        error: function(req, err){ }
    })
}

function onSuccess(data){
    
}

