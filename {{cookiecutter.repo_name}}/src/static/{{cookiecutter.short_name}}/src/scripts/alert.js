$( document ).ready(function() {
    $( ".alert__close-button" ).on('click', function() {
        $(this).parent('.alert').remove();
    });
});
