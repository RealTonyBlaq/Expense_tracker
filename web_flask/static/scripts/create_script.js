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
                    $('#emailAvailability').html('<i class="fas fa-exclamation-triangle"></i> &nbsp; email already exists').css({
                        'color': 'red',
                        'border': 'none',
                        'font-size': '12px',
                        'margin-right': '160px'
                      });
                    $('#email').css({
                        'border': '1px solid red'
                    });
                    $('#submitBtn').prop('disabled', true);
                },
                error: function(xhr, status, error) {
                    if (xhr.status === 404) {
                        $('#emailAvailability').html('<i class="fas fa-check-circle"></i> &nbsp; email available').css({
                            'color': 'green',
                            'border': 'none',
                            'font-size': '12px',
                            'margin-right': '180px'
                        });
                        $('#email').css({
                            'border': '1px solid green'
                        });
                        $('#submitBtn').prop('disabled', false);
                    } else {
                        $('#emailAvailability').html('<i class="fas fa-exclamation-triangle"></i> &nbsp; Error occurred while checking email availability').css({
                            'color': 'red',
                            'border': 'none',
                            'font-size': '10px',
                            'margin-right': '30px'
                          });
                        $('#email').css({
                            'border': '1px solid red'
                        });
                        $('#submitBtn').prop('disabled', true);
                    }
                }
            });
        }
    });
    $('#password').on('keyup', function () {
        const pwd = $('#password').val();
        if (/[a-z]/.test(pwd)) {
            $('#smallLetter').html('<i class="fas fa-check-circle"></i> &nbsp; small alphabets').css({
                'color': 'green',
                'border': 'none',
                'font-size': '12px',
                'margin-right': '180px'
            });
        } else {
            $('#smallLetter').html('<i class="fas fa-exclamation-triangle"></i> &nbsp; Small alphabets').css({
                'color': 'red',
                'border': 'none',
                'font-size': '12px',
                'margin-right': '180px'
            });
        }
        if (/[A-Z]/.test(pwd)) {
            $('#capLetter').html('<i class="fas fa-check-circle"></i> &nbsp; At least one Capital letter').css({
                'color': 'green',
                'border': 'none',
                'font-size': '12px',
                'margin-right': '125px'
            });
        } else {
            $('#capLetter').html('<i class="fas fa-exclamation-triangle"></i> &nbsp; At least one Capital letter').css({
                'color': 'red',
                'border': 'none',
                'font-size': '12px',
                'margin-right': '125px'
            });
        }
        if (/[0-9]/.test(pwd)) {
            $('#number').html('<i class="fas fa-check-circle"></i> &nbsp; At least one digit').css({
                'color': 'green',
                'border': 'none',
                'font-size': '12px',
                'margin-right': '175px'
            });
        } else {
            $('#number').html('<i class="fas fa-exclamation-triangle"></i> &nbsp; At least one digit').css({
                'color': 'red',
                'border': 'none',
                'font-size': '12px',
                'margin-right': '175px'
            });
        }
        if (/[!@#$%^&*()]/.test(pwd)) {
            $('#specialCharacter').html('<i class="fas fa-check-circle"></i> &nbsp; At least one special character [!,@,#,$,%,^,&,*,(,)]').css({
                'color': 'green',
                'border': 'none',
                'font-size': '12px',
                'margin-right': '100px'
            });
        } else {
            $('#specialCharacter').html('<i class="fas fa-exclamation-triangle"></i> &nbsp; At least one special character [!,@,#,$,%,^,&,*,(,)]').css({
                'color': 'red',
                'border': 'none',
                'font-size': '12px',
                'margin-right': '100px'
            });
        }
        if (pwd.length >= 8) {
            $('#pwdLength').html('<i class="fas fa-check-circle"></i> &nbsp; Password length at least 8 characters').css({
                'color': 'green',
                'border': 'none',
                'font-size': '12px',
                'margin-right': '50px'
            });
        } else {
            $('#pwdLength').html('<i class="fas fa-exclamation-triangle"></i> &nbsp; Password length at least 8 characters').css({
                'color': 'red',
                'border': 'none',
                'font-size': '12px',
                'margin-right': '50px'
            });
        }
    });

    $('#submitBtn').on('click', function (event) {
      const lname = $('#lastName').val();
      const fname = $('#firstName').val();
      const pwd = $('#password').val();
      if (/[!@#$%^&.*(){}]/.test(lname)) {
        event.preventDefault();
        $('#checkLastName').html('<i class="fas fa-exclamation-triangle"></i> &nbsp; Last name must contain only alphabets').css({
          'color': 'red',
          'border': 'none',
          'font-size': '10px',
          'margin-right': '150px'
        });
        $('#lastName').css({
            'border': '1px solid red'
        });
      } else {
        $('#checkLastName').remove();
        $('#lastName').css({
            'border': '1px solid #add'
        });
      }
      if (/[!@#$%^&.*(){}]/.test(fname)) {
        event.preventDefault();
        $('#checkFirstName').html('<i class="fas fa-exclamation-triangle"></i> &nbsp; First name must contain only alphabets').css({
            'color': 'red',
            'border': 'none',
            'font-size': '10px',
            'margin-right': '150px'
        });
        $('#firstName').css({
            'border': '1px solid red'
        });
      } else {
        $('#checkFirstName').remove();
        $('#firstName').css({
            'border': '1px solid #add'
        });
      }
      if (/[a-z]/.test(pwd) && /[A-Z]/.test(pwd) && /[0-9]/.test(pwd) && /[!@#$%^&*()]/.test(pwd) && pwd.length >= 8) {
        $('#password').css({
            'border': '1px solid green'
        });
      } else {
        event.preventDefault();
        $('#password').css({
            'border': '1px solid red'
        });
      }
    });
});
