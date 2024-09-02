$(document).ready(function () {
    $('#email').on('keyup', function () {
        const email = $(this).val();
        const atPosition = email.indexOf('@');
        const dotPosition = email.lastIndexOf('.');
        const dotcheck = dotPosition > atPosition && email.substring(dotPosition + 1).length >= 2;
        
        if (atPosition > 0 && dotPosition > atPosition + 1 && dotcheck) {
            $.ajax({
                url: `http://127.0.0.1:5000/api/users/email/${email}`,
                method: 'GET',
                dataType: 'json',
                success: function (response) {
                    $('#email').css({
                        'border-bottom': '2px solid green',
                        'border-right': '2px solid green'
                    });
                    $('#submitBtn').prop('disabled', false);
                    $('#getCodeButton').prop('disabled', false);
                },
                error: function (xhr) {
                    if (xhr.status === 404) {
                        $('#email').css({
                            'border-bottom': '2px solid red',
                            'border-right': '2px solid red'
                        });
                        $('#submitBtn').prop('disabled', true);
                        $('#getCodeButton').prop('disabled', true);
                    } else {
                        alert(`Error occurred.. Try again [${xhr.responseText}]`);
                        $('#submitBtn').prop('disabled', true);
                        $('#getCodeButton').prop('disabled', true);
                    }
                }
            });
        } else {
            $('#email').css({
                'border-bottom': '',
                'border-right': ''
            });
            $('#submitBtn').prop('disabled', true);
            $('#getCodeButton').prop('disabled', true);
        }
    });

    $('#getCodeButton').on('click', function () {

    });
});
