$(document).ready (function () {
    // getUserDetails();
    $('#edit').click(function(){
        $('#password').prop('readonly', false);
        $('#displayName').prop('readonly', false);
        $('#email').prop('readonly', false);
        $('#phone').prop('readonly', false);
        $('#description').prop('readonly', false);
        $('#price').prop('readonly', false);
        $('#password').val('');
        $('#displayName').val('');
        $('#email').val('');
        $('#phone').val('');
        $('#price').val('');
        $('#description').val('');
        $('#save-btn').removeAttr('hidden');
        $('#edit').prop('hidden', 'hidden');
        if ($('#type').val()=="Venue") {
            $('#address').val('');
            $('#address').prop('readonly', false);
        }
    });
});

function getUserDetails(ajaxurl) {
    $.ajax({
        method: 'GET',
        url: "/partyup/user_profile",
        success: onSuccess,
        error: function(req, err){  }
    })
}

function onSuccess(data){
    // log.console(data[0].email);
    $( "#displayName" ).val( data[0].display_name );
    $( "#email" ).val( data[0].email );
    $( "#phone" ).val( data[0].phone_number );
}

