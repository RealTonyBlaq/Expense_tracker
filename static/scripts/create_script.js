$(document).ready(function () {
  $('#accountForm').submit(function (event) {
    event.preventDefault();
    const username = $('#username').val();
    const email = $('#email').val();
    const password = $('#password').val();
    $.ajax({
      url: 'http://127.0.0.1:5000/api/users',
      method: "POST",
      data: JSON.stringify({
        first_name: username,
        last_name: username,
        email: email,
        password: password
      }),
      headers: {
        "Content-Type": "application/json"
      },
      success: function () {
        alert('New account created successfully');
      },
      error: function (xhr, status, error) {
        alert(xhr.responseText);
      }
    });
  });
});
