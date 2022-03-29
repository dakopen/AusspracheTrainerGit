const dropdown = $("#dropdown");
const textarea = $("#textarea");
const textareaError = $("#textarea-error");
var sessionId = null;


var textareaMaxWidth = null;
var textareaWidth = null;

windowResize();
/* EVENT LISTENERS */
textarea.on('input change keyup paste', resizeTextarea);
$(window).resize(windowResize);
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


function resizeTextarea() {
    let computedFontSize = textarea.css("font-size");
    let fontAttr = "400 " + String(Math.max(Math.min(parseInt(computedFontSize) + 1, 50), 30)) + "px Open Sans";
    textwidth = getTextWidth(textarea.val(), fontAttr);
    textarea.width(Math.max(textareaWidth, Math.min(textwidth + (parseInt(computedFontSize) + 1 - 36.8), window.innerWidth * 0.95)) + 'px');

    textarea.css("height", "1.6em");
    textarea.css("height", textarea.prop("scrollHeight") + "px");
    checkTextareaInputServerside(textarea.val());
}

function windowResize() {
    textareaMaxWidth = Math.min(window.innerWidth * 0.85, 750);
    textarea.css("max-width", textareaMaxWidth + "px");
    textareaWidth = Math.min(window.innerWidth * 0.85, 450);
    resizeTextarea();
}


function getTextWidth(text, font) {
    // re-use canvas object for better performance
    const canvas = getTextWidth.canvas || (getTextWidth.canvas = document.createElement("canvas"));
    const context = canvas.getContext("2d");
    context.font = font;
    const metrics = context.measureText(text);
    return metrics.width;
}


function satzGenerieren() {
    let selectedCategory = dropdown.find("input").val();
    console.log(selectedCategory);

    parameterUrl = `/satzgenerator/?session=${sessionId}/`
    fetch(parameterUrl, {
        method: "post", body: selectedCategory,
        headers: {
            "X-CSRFToken": getCookie("csrftoken"),
            "currenttextarea": textarea.val(),
        }
    }).then(function (data) {
        data.text().then(function (text) {
            textarea.val(text);
            resizeTextarea();
        })
    }
    )
}

function checkTextareaInput(text) {
    if (text.length > 120) {
        textarea.val(text.substring(0, 120));
    }
    // Text von Sonderzeichen entfernen
    text = text.replace(/\s\s+/g, ' ').replace(/[`~!@^*()_|+\-=?;:'",.<>\{\}\[\]\\\/]/gi, '').trim();
    let fehlerListe = []

    if (text.match("[^a-zA-ZäöüÄÖÜß0-9 \s\x21-\x2F\x3A-\x40\x5B-\x60\x7B-\x7E]")) { // nicht-deutsche Zeichen verwendet
        fehlerListe.push("Bitte nur deutsches Alphabet verwenden.")
    }
    if (/\d/.test(text)) { // Zahlen verwendet
        fehlerListe.push("Bitte Zahlen ausschreiben.")
    }
    if (text.match("[#%&$€\x23-\x26]")) {
        fehlerListe.push("Bitte Sonderzeichen ausschreiben.")
    }
    const longerThan25 = (element) => element.length > 25;
    if (text.split(" ").some(longerThan25)) {
        fehlerListe.push("Kein Wort darf länger als 25 Buchstaben lang sein.")
    }
    /*displayTextareaError(fehlerListe);*/
}

function displayTextareaError(fehlerListe) {
    var textareaErrorText = ""
    fehlerListe.forEach(function (item, index) {
         textareaErrorText += item + " "
      });
    textareaError.html(textareaErrorText.trim())
}

function checkTextareaInputServerside(text) {
    if (sessionId != null) {
        parameterUrl = `/satzcheck/?session=${sessionId}/`
        fetch(parameterUrl, {
            method: "post", body: text,
            headers: {
                "X-CSRFToken": getCookie("csrftoken"),
            }
        }).then(response => response.json())
        .then(data => displayTextareaError(data));
        
        

        
    }
}