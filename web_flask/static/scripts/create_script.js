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
                        $('#emailAvailability').html('<i class="fas fa-exclamation-triangle"></i>  Error occurred while checking email availability').css({
                            'color': 'red',
                            'border': '1px dashed black',
                            'font-size': '10px',
                            'margin-right': '30px',
                            'border-radius': '10px'
                          });
                        $('#submitBtn').prop('disabled', true);
                    }
                }
            });
        }
    });
    $('#password').on('keyup', function () {
        const pwd = $('#password').val()
        if (/[a-z]/.test(pwd)) {
            $('#smallLetter').html('<i class="fas fa-check-circle"></i>  small alphabets').css({
                'color': 'green',
                'border': '1px dashed black',
                'font-size': '12px',
                'margin-right': '180px',
                'border-radius': '10px'
            });
        } else {
            $('#smallLetter').html('<i class="fas fa-exclamation-triangle"></i>  Small alphabets').css({
                'color': 'orange',
                'border': '1px dashed black',
                'font-size': '12px',
                'margin-right': '180px',
                'border-radius': '10px'
            });
        }
        if (/[A-Z]/.test(pwd)) {
            $('#capLetter').html('<i class="fas fa-check-circle"></i>  At least one Capital letter').css({
                'color': 'green',
                'border': '1px dashed black',
                'font-size': '12px',
                'margin-right': '125px',
                'border-radius': '10px'
            });
        } else {
            $('#capLetter').html('<i class="fas fa-exclamation-triangle"></i>  At least one Capital letter').css({
                'color': 'orange',
                'border': '1px dashed black',
                'font-size': '12px',
                'margin-right': '125px',
                'border-radius': '10px'
            });
        }
        if (/[0-9]/.test(pwd)) {
            $('#number').html('<i class="fas fa-check-circle"></i>  At least one digit').css({
                'color': 'green',
                'border': '1px dashed black',
                'font-size': '12px',
                'margin-right': '170px',
                'border-radius': '10px'
            });
        } else {
            $('#number').html('<i class="fas fa-exclamation-triangle"></i>  At least one digit').css({
                'color': 'orange',
                'border': '1px dashed black',
                'font-size': '12px',
                'margin-right': '170px',
                'border-radius': '10px'
            });
        }
        if (/[!@#$%^&*()]/.test(pwd)) {
            $('#specialCharacter').html('<i class="fas fa-check-circle"></i>  At least one special character !,@,#,$,%,^,&,*,(,)').css({
                'color': 'green',
                'border': '1px dashed black',
                'font-size': '12px',
                //'margin-right': '180px',
                'border-radius': '10px'
            });
        } else {
            $('#specialCharacter').html('<i class="fas fa-exclamation-triangle"></i>  At least one special character !,@,#,$,%,^,&,*,(,)').css({
                'color': 'orange',
                'border': '1px dashed black',
                'font-size': '12px',
                //'margin-right': '180px',
                'border-radius': '10px'
            });
        }
        if (pwd.length >= 8) {
            $('#pwdLength').html('<i class="fas fa-check-circle"></i>  Password length at least 8 characters').css({
                'color': 'green',
                'border': '1px dashed black',
                'font-size': '12px',
                'margin-right': '50px',
                'border-radius': '10px'
            });
        } else {
            $('#pwdLength').html('<i class="fas fa-exclamation-triangle"></i>  Password length at least 8 characters').css({
                'color': 'orange',
                'border': '1px dashed black',
                'font-size': '12px',
                'margin-right': '50px',
                'border-radius': '10px'
            });
        }
    });
});
