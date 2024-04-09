$(document).ready(function () {
    $('#email').on('keyup', function() {
        const email = $(this).val();
        // Send AJAX request to check email availability
        if (email.includes('@') && email.includes('.')) {
            $.ajax({
                url: `http://127.0.0.1:5000/api/users/email/${email}`,
                method: 'GET',
                dataType: 'json',
                success: function(response) {
                    $('#emailAvailability').html('<i class="fas fa-exclamation-triangle"></i>   email already exists').css({
                        'color': 'red',
                        'border': '1px dashed black',
                        'font-size': '12px',
                        'margin-right': '160px',
                        'border-radius': '10px'
                      });
                    $('#submitBtn').prop('disabled', true);
                },
                error: function(xhr, status, error) {
                    if (xhr.status === 404) {
                        $('#emailAvailability').html('<i class="fas fa-check-circle"></i>     email available').css({
                            'color': 'green',
                            'border': '1px dashed black',
                            'font-size': '12px',
                            'margin-right': '180px',
                            'border-radius': '10px'
                        });
                        $('#submitBtn').prop('disabled', false);
                    } else {
                        $('#emailAvailability').text('Error occurred while checking email availability').css('color', 'red');
                        $('#submitBtn').prop('disabled', true);
                    }
                }
            });
        }
    });
});
