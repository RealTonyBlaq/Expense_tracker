$(document).ready(function () {
    $('#email').on('keyup', function() {
        const email = $(this).val();
        // Send AJAX request to check email availability
        $.ajax({
            url: `http://127.0.0.1:5000/api/users/email/${email}`,
            method: 'GET',
            dataType: 'json',
            success: function(response) {
                $('#emailAvailability').text('email already exists').css('color', 'red');
                $('#submitBtn').prop('disabled', true);
            },
            error: function(xhr, status, error) {
                if (xhr.status === 404) {
                    $('#emailAvailability').text('email available').css({'color': 'green'});
                    $('#submitBtn').prop('disabled', false);
                } else {
                    $('#emailAvailability').text('Error occurred while checking email availability').css('color', 'red');
                }
            }
        });
    });
});
