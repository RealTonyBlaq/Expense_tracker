$(document).ready(function () {
  $('#accountForm').submit(function (event) {
    event.preventDefault();
    const firstName = $('#firstName').val();
    const lastName = $('#lastName').val();
    const email = $('#email').val();
    const password = $('#password').val();
    $.ajax({
      url: 'http://127.0.0.1:5000/api/users',
      method: 'POST',
      data: JSON.stringify({
        first_name: firstName,
        last_name: lastName,
        email: email,
        password: password
      }),
      headers: {
        'Content-Type': 'application/json'
      },
      success: function () {
        console.log('New account created successfully');
        window.location.href = 'signin.html';
      },
      error: function (xhr, status, error) {
        console.log(xhr.responseText);
      }
    });
  });
});
