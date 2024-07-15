$(document).ready(function () {
    function setStatus(element, icon, message, color, marginRight) {
        $(element).html(`${icon} &nbsp; ${message}`).css({
            'color': color,
            'border': 'none',
            'font-size': '12px',
            'margin-right': marginRight
        });
    }

    function setBorder(element, color) {
        $(element).css({
            'border': `1px solid ${color}`
        });
    }

    function validateName(name, element, errorElement) {
        const regex = /[!@#$%^&.*(){}]/;
        if (regex.test(name)) {
            setStatus(errorElement, '<i class="fas fa-exclamation-triangle"></i>', 'Name must contain only alphabets', 'red', '150px');
            setBorder(element, 'red');
            return false;
        } else {
            $(errorElement).empty();
            setBorder(element, '#add');
            return true;
        }
    }

    $('#email').on('keyup', function () {
        const email = $(this).val();
        if (email.includes('@') && email.includes('.')) {
            $.ajax({
                url: `http://127.0.0.1:5000/api/users/email/${email}`,
                method: 'GET',
                dataType: 'json',
                success: function (response) {
                    setStatus('#emailAvailability', '<i class="fas fa-exclamation-triangle"></i>', 'Email already exists', 'red', '160px');
                    setBorder('#email', 'red');
                    $('#submitBtn').prop('disabled', true);
                },
                error: function (xhr) {
                    if (xhr.status === 404) {
                        setStatus('#emailAvailability', '<i class="fas fa-check-circle"></i>', 'Email available', 'green', '180px');
                        setBorder('#email', 'green');
                        $('#submitBtn').prop('disabled', false);
                    } else {
                        setStatus('#emailAvailability', '<i class="fas fa-exclamation-triangle"></i>', 'Error occurred while checking email availability', 'red', '30px');
                        setBorder('#email', 'red');
                        $('#submitBtn').prop('disabled', true);
                    }
                }
            });
        }
    });

    $('#password').on('keyup', function () {
        const password = $(this).val();
        const criteria = [
            { regex: /[a-z]/, element: '#smallLetter', message: 'small alphabets', marginRight: '180px' },
            { regex: /[A-Z]/, element: '#capLetter', message: 'At least one Capital letter', marginRight: '125px' },
            { regex: /[0-9]/, element: '#number', message: 'At least one digit', marginRight: '175px' },
            { regex: /[!@#$%^&*()]/, element: '#specialCharacter', message: 'At least one special character [!,@,#,$,%,^,&,*,(,)]', marginRight: '100px' },
            { regex: /.{8,}/, element: '#pwdLength', message: 'Password length at least 8 characters', marginRight: '50px' }
        ];

        criteria.forEach(criterion => {
            if (criterion.regex.test(password)) {
                setStatus(criterion.element, '<i class="fas fa-check-circle"></i>', criterion.message, 'green', criterion.marginRight);
            } else {
                setStatus(criterion.element, '<i class="fas fa-exclamation-triangle"></i>', criterion.message, 'red', criterion.marginRight);
            }
        });
    });

    $('#submitBtn').on('click', function (event) {
        const lastName = $('#lastName').val();
        const firstName = $('#firstName').val();
        const password = $('#password').val();

        const isLastNameValid = validateName(lastName, '#lastName', '#checkLastName');
        const isFirstNameValid = validateName(firstName, '#firstName', '#checkFirstName');
        const isPasswordValid = /[a-z]/.test(password) && /[A-Z]/.test(password) && /[0-9]/.test(password) && /[!@#$%^&*()]/.test(password) && password.length >= 8;

        if (!isLastNameValid || !isFirstNameValid || !isPasswordValid) {
            event.preventDefault();
            if (!isPasswordValid) {
                setBorder('#password', 'red');
            }
        } else {
            setBorder('#password', 'green');
        }
    });
});
