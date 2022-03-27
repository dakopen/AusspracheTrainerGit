const dropdown = $("#dropdown");
const textarea = $("#textarea");

var sessionId = null;



//JQUERY
/* PAGE LOAD */
(function ($) {
    "use strict";
    // Page loading animation
    $(window).on("load", function () {
        $("#js-preloader").addClass("loaded");
        sessionId = makeid();
        console.log("Session-ID: " + sessionId);
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

function toggleDropdown() {
    dropdown.attr('tabindex', 1).focus();
    dropdown.toggleClass("active");
    dropdown.find(".dropdown-menu").slideToggle(300);
}

function dropdownFold() {
    console.log("fold");
    dropdown.removeClass("active");
    dropdown.find(".dropdown-menu").slideUp(300);

}

/* Funktion: Dropdown-Item pressed */
$('.dropdown .dropdown-menu li').click(function () {
    dropdown.find("span").text($(this).attr("content"));
    dropdown.find("input").attr("value", $(this).attr("content"))
});


/* get Cookie */
function getCookie(name) {
    var cookieValue = null;
    if (document.cookie && document.cookie !== "") {
        var cookies = document.cookie.split(";");
        for (var i = 0; i < cookies.length; i++) {
            var cookie = cookies[i].trim();
            if (cookie.substring(0, name.length + 1) === (name + "=")) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}

/*
function satzGeneratorBackend(data)
{parameterUrl="/satzgenerator/?session="+sessionid;
console.log(parameterUrl);
fetch(parameterUrl,
    {method:"post",
    body:data,
    headers: {"X-CSRFToken":getCookie('csrftoken'),"TEXTAREAVALUE":textarea.value.replace(/\s+/g,' ').trim(),},})
.then(function(data){data.text().then(text=>{textarea.value=text;windowResize();resizeTextArea();});});}

*/

function satzGenerieren() {
    let selectedCategory = dropdown.find("input").val();
    console.log(selectedCategory);

    parameterUrl = `/satzgenerator/?session=${sessionId}/`
    fetch(parameterUrl, {
        method: "post", body: selectedCategory,
        headers: {
            "X-CSRFToken": getCookie("csrftoken"),
            "currenttextarea": sonderzeichenEntfernen(textarea.val()),

        }
    }).then(function (data) {
        data.text().then(function (text) {
            textarea.val(text);
            
            //Textarea resize!

        })

    }
    )
}

function sonderzeichenEntfernen(text){
    console.log(text.toLowerCase().replace(/[^a-zA-Z ]/g, ""))
    return text.toLowerCase().replace(/[^a-z ]/g, "")
}

