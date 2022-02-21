
//JQUERY
/* PAGE LOAD */
(function($) {

    "use strict";
    // Page loading animation
    $(window).on('load', function() {
        $('#js-preloader').addClass('loaded');
        sessionid = makeid();
    });

})(window.jQuery);


/* SESSION ID */
// https://stackoverflow.com/questions/48095737/django-new-session-for-each-browser-tab/48112774
function makeid() {
    var text = "";
    var possible = "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789";

    for (var i = 0; i < 6; i++)
        text += possible.charAt(Math.floor(Math.random() * possible.length));
    return text;
}
