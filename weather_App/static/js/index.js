$(document).ready(function() {
    $('.header__text').slideUp().slideDown();

    // Alert message animation
    setTimeout(function() {
        $('#message').fadeOut('slow');
    }, 4000);

});