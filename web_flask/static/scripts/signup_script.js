function togglePasswordVisibility() {
    const passwordField = document.getElementById('password');
    const toggleIcon = document.getElementById('toggleIcon');
    
    if (passwordField.type === 'password') {
        passwordField.type = 'text';
        toggleIcon.classList.remove('fa-eye');
        toggleIcon.classList.add('fa-eye-slash');
    } else {
        passwordField.type = 'password';
        toggleIcon.classList.remove('fa-eye-slash');
        toggleIcon.classList.add('fa-eye');
    }
}

$(document).ready(function () {
    $('#email').on('keyup', function () {
        const email = $(this).val();
        const dotcheck = email.split('.')[1].length >= 2;
        if (email.includes('@') && email.includes('.') && dotcheck) {
            $.ajax({
                url: `http://172.25.180.166:5000/api/users/email/${email}`,
                method: 'GET',
                dataType: 'json',
                success: function (response) {
                    //setStatus('#emailAvailability', '<i class="fas fa-exclamation-triangle"></i>', 'Email already in use', 'red', '160px');
                    //setBorder('#email', 'red');
                    $('#email').css({
                        'border-bottom': '2px solid red',
                        'border-right': '2px solid red'
                    });
                    $('#submitBtn').prop('disabled', true);
                },
                error: function (xhr) {
                    if (xhr.status === 404) {
                        //setStatus('#emailAvailability', '<i class="fas fa-check-circle"></i>', 'Email available', 'green', '180px');
                        //setBorder('#email', 'green');
                        $('#email').css({
                            'border-bottom': '2px solid green',
                            'border-right': '2px solid green'
                        });
                        $('#submitBtn').prop('disabled', false);
                    } else {
                        //setStatus('#emailAvailability', '<i class="fas fa-exclamation-triangle"></i>', 'Error occurred while checking email availability', 'red', '30px');
                        //setBorder('#email', 'red');
                        alert(`Error occurred.. Try again [${xhr.responseText}]`)
                        $('#submitBtn').prop('disabled', true);
                    }
                }
            });
        } else {
            $('#submitBtn').prop('disabled', true);
        }
    });

    $('#password').on('keyup', function () {
        const password = $(this).val();

        const isPasswordValid = /[a-z]/.test(password) && /[A-Z]/.test(password) && /[0-9]/.test(password) && /[!@#$%^&*()]/.test(password) && password.length >= 8;
        if (!isPasswordValid) {
            $('#password').css({
                'border-right': '2px solid red',
                'border-bottom': '2px solid red'
            });
            $('#submitBtn').prop('disabled', true);
        } else {
            $('#password').css({
                'border-right': '2px solid green',
                'border-bottom': '2px solid green'
            });
            $('#submitBtn').prop('disabled', false);
        }
    });

    $('#submitBtn').on('click', function (event) {
        event.preventDefault();
        const last_name = $('#lastName').val();
        const first_name = $('#firstName').val();
        const email = $('#email').val();
        const password = $('#password').val();

        const userData = {
            last_name,
            first_name,
            email,
            password,
        };

        $.ajax({
            url: 'http://172.25.180.166:5000/api/users',
            type: 'POST',
            contentType: 'application/json',
            dataType: 'json',
            data: JSON.stringify(userData),
            success: function (response) {
                $('#redirect').html('Success. You will be automatically redirected in 3 secs');
                setTimeout(function () {
                    window.location.href = "/signin";
                }, 3000);
            },
            error: function (xhr) {
                $('#redirect').html(`Error occurred. Please try again! [${xhr.responseText}]`).css({
                    'color': 'red',
                });
            }
        });
    });
});
