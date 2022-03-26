const dropdown = $('.dropdown');





//JQUERY
/* PAGE LOAD */
(function($) {

    "use strict";
    // Page loading animation
    $(window).on('load', function() {
        $('#js-preloader').addClass('loaded');
        var sessionid = makeid();
        console.log("Session-ID: " + sessionid);
    });

})(window.jQuery);


/* SESSION ID */
// https://stackoverflow.com/questions/48095737/django-new-session-for-each-browser-tab/48112774
function makeid() {
    var text = "";
    var possible = "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789";

    for (var i = 0; i < 8; i++)
        text += possible.charAt(Math.floor(Math.random() * possible.length));
    return text;
}

function generieren(){let generierobjekt=dropdown.find('input').val();let response=satzGeneratorBackend(generierobjekt);}
function satzGeneratorBackend(data){parameterUrl="/satzgenerator/?session="+sessionid;console.log(parameterUrl)
fetch(parameterUrl,{method:"post",body:data,headers:{"X-CSRFToken":getCookie('csrftoken'),"TEXTAREAVALUE":textarea.value.replace(/\s+/g,' ').trim(),},}).then(function(data){data.text().then(text=>{textarea.value=text;windowResize();resizeTextArea();});});}
/* GENERATOR */
function generieren() {

}
