
window.onload = function() {

    $('.submit').click(function() {

        var name = $('#NAME_INPUT').val();
        var email = $('#EMAIL_INPUT').val();
        var confirmEmail = $('#CONFIRM_EMAIL_INPUT').val();

        if (!email.includes('@')) {
            alert('Email must contain @');
        }

        if (email !== confirmEmail) {
            alert('Emails must match');
            return;
        }

        $.post('/api/v1/register', {
            name: name,
            email: email
        }, function(data) {
            var number = JSON.parse(data);

            var faxTo = $('.fax-to').text()
                .replace('{number}', number.number)
                .replace('{email}', number.email);
            var faxFrom = $('.fax-from').text()
                .replace('{number}', number.number)
                .replace('{email}', number.email);

            $('.fax-to').text(faxTo);
            $('.fax-from').text(faxFrom);

            $('.content, .finish').toggleClass('hidden');
        }).fail(function() {
            $('.content, .error').toggleClass('hidden');
        });

    });

};