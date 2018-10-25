$(document).ready(function() {

    $('#card-register').submit(function(event) {

        var formData = {
            'register': $('input[name=register]').val()
        };

        $.ajax({
            type        : 'POST',
            url         : '/index/cardRegister', 
            data        : formData, 
            dataType    : 'json', 
            encode      : true
        })
            .done(function(data) {
                window.location.href = '/';
            });

        event.preventDefault();
    });

});