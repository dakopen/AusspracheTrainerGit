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



/*dropdown.click(function(){$(this).attr('tabindex',1).focus();
$(this).toggleClass('active');
$(this).find('.dropdown-menu').slideToggle(300);});
$('.dropdown').focusout(function(){$(this).removeClass('active');
$(this).find('.dropdown-menu').slideUp(300);});

$('.dropdown .dropdown-menu li').click(function(){$(this).parents('.dropdown').find('span').text($(this).text());
$(this).parents('.dropdown').find('input').attr('value',$(this).attr('content'));});
function clearTextarea(){textarea.value="";resizeTextArea();textarea.focus();weiterueben_verstecken();}

*/
//function generieren(){let generierobjekt=dropdown.find('input').val();let response=satzGeneratorBackend(generierobjekt);}
//function satzGeneratorBackend(data){parameterUrl="/satzgenerator/?session="+sessionid;console.log(parameterUrl)
//fetch(parameterUrl,{method:"post",body:data,headers:{"X-CSRFToken":getCookie('csrftoken'),"TEXTAREAVALUE":textarea.value.replace(/\s+/g,' ').trim(),},}).then(function(data){data.text().then(text=>{textarea.value=text;windowResize();resizeTextArea();});});}
/* GENERATOR */




function toggle_dropdown(){
    dropdown.attr('tabindex',1).focus();
    dropdown.toggleClass("active");
    dropdown.find(".dropdown-menu").slideToggle(300);
}
  
function dropdown_fold(){
    console.log("fold");
    dropdown.removeClass("active");
    dropdown.find(".dropdown-menu").slideUp(300);

}

/* Funktion: Dropdown-Item pressed */
$('.dropdown .dropdown-menu li').click(function(){
    dropdown.find("span").text($(this).attr("content"));
    dropdown.find("input").attr("value", $(this).attr("content"))

});




/*
$(this).parents('.dropdown').find('input').attr('value',$(this).attr('content'));});

*/


function generieren() {
    let selected_category = dropdown.find("input").val();
    console.log(selected_category);
}
