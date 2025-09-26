$(document).ready(function() {
    $('#login-reset-button').click(function(e) {
        e.preventDefault();

        $.ajax({
            url: '/login',
            method: 'POST',
            data: {
                username: $('#username').val(),
                password: $('#password').val()
            },
            success: function(response) {
                if (response.redirect) {
                    window.location.href = response.redirect;
                } else {
                    alert(response.message);
                }
            }
        });
    });
});