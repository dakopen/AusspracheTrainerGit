const dropdown = $("#dropdown");
const textarea = $("#textarea");
const textareaError = $("#textarea-error");
const binIcon = $("#bin-icon");
const mikrofonIcon = $("#mikrofon-icon");
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
        sessionId = retrieveId();
        console.log("Session-ID: " + sessionId);
        clearTextarea();
        console.log("CSRF-Token: " + getCookie("csrftoken"));
    });

})(window.jQuery);


/* SESSION ID */
// https://stackoverflow.com/questions/48095737/django-new-session-for-each-browser-tab/48112774
function retrieveId() {
    return document.getElementById("sessionId").value
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

function setCookie(name, value, days) {
    var expires = "";
    if (days) {
        var date = new Date();
        date.setTime(date.getTime() + (days * 24 * 60 * 60 * 1000));
        expires = "; expires=" + date.toUTCString();
    }
    document.cookie = name + "=" + (value || "") + expires + "; path=/;SameSite=Lax";
}


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

    parameterUrl = `/satzgenerator/?session=${sessionId}`
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


/* CLIENT SIDE */
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
    displayTextareaError(fehlerListe);
}

function displayTextareaError(fehlerListe) {
    var textareaErrorText = ""
    fehlerListe.forEach(function (item, index) {
        textareaErrorText += item + " "
    });
    textareaError.html(textareaErrorText.trim())
}

/* SERVER SIDE */
function checkTextareaInputServerside(text) {
    if (sessionId != null) {
        parameterUrl = `/satzcheck/?session=${sessionId}`
        fetch(parameterUrl, {
            method: "post",
            body: text,
            headers: {
                "X-CSRFToken": getCookie("csrftoken"),
                mode: "same-origin"
            }
        }).then(response => response.json())
            .then(data => {
                displayTextareaError(data[0]);
                if (data[1]) {
                    binIcon.addClass("active");
                    binIcon.removeClass("inactive")
                }
                else {
                    binIcon.removeClass("active");
                    binIcon.addClass("inactive");
                };
            }
            );
    }
}

function clearTextarea() {
    textarea.val("");
    resizeTextarea();
}

/* AUDIO */
// see: https://blog.addpipe.com/using-recorder-js-to-capture-wav-audio-in-your-html5-web-site/

//webkitURL is deprecated but nevertheless 
URL = window.URL || window.webkitURL;
var gumStream;
//stream from getUserMedia() 
var rec;
//Recorder.js object 
var input;
//MediaStreamAudioSourceNode we'll be recording 
// shim for AudioContext when it's not avb. 
var AudioContext = window.AudioContext || window.webkitAudioContext;
var audioContext;
var recordingsList = document.getElementById("recordingsList");

function toggleRecording() {
    try {
        if (rec.recording) { stopRecording(); }
        else { startRecording(); }
    }
    catch (TypeError) {
        startRecording();
    }
}

function startRecording() {
    navigator.mediaDevices.getUserMedia({ audio: true, video: false }).then(function (stream) {
        console.log("getUserMedia() success, stream created, initializing Recorder.js ...");

        /* Aktives Mikrofon Bild */
        mikrofonIcon.attr("src", "/static/assets/images/Mikrofon_aktiv.svg");
        mikrofonIcon.css({ "width": "80%", "height": "80%" });
        /* assign to gumStream for later use */
        audioContext = new AudioContext();

        gumStream = stream;
        /* use the stream */

        input = audioContext.createMediaStreamSource(stream);
        /* Create the Recorder object and configure to record mono sound (1 channel) Recording 2 channels will double the file size */
        rec = new Recorder(input, {
            numChannels: 1
        })
        //start the recording process 
        rec.record()
        console.log("Aufnahme gestartet...");
        aufnahmeTimeout = setTimeout(function () {
            console.log("Aufnahme-Timeout");
            stopRecording();
        }, 22000);





    }).catch(function (err) {
        //enable the record button if getUserMedia() fails 
        console.log("getUserMedia() fehlgeschlagen.");
    });
}

function stopRecording() {
    //tell the recorder to stop the recording
    if (rec.recording) {
        clearTimeout(aufnahmeTimeout);
        mikrofonIcon.attr("src", "static/assets/images/Mikrofon.svg");
        mikrofonIcon.css({ "width": "62%", "height": "62%" });

        rec.stop(); //stop microphone access
        gumStream.getAudioTracks()[0].stop();
        //create the wav blob and pass it on to createDownloadLink 
        rec.exportWAV(createDownloadLink);
        rec.exportWAV(sendData);
        console.log("Aufnahme beendet.");
    }
}

function createDownloadLink(blob) {
    var url = URL.createObjectURL(blob);
    var au = document.createElement('audio');
    var li = document.createElement('li');
    var link = document.createElement('a');
    //add controls to the <audio> element 
    au.controls = true;
    au.src = url;
    //link the a element to the blob 
    link.href = url;
    link.download = new Date().toISOString() + '.wav';
    link.innerHTML = link.download;
    //add the new audio and a elements to the li element 
    li.appendChild(au);
    li.appendChild(link);
    //add the li element to the ordered list 
    recordingsList.appendChild(li);
    console.log("Aufnahme exportiert.");
}

/* SPÄTER: erneutes Anhören */
function createAudioObject(blob) {
    var url = URL.createObjectURL(blob);
    audioObjectListenAgain = document.createElement('audio');
    audioObjectListenAgain.controls = true;
    audioObjectListenAgain.src = url;
}   // ENDE SPÄTER


function sendData(data) {
    createAudioObject(data);
    console.log("Sendet Audio Dateien ans Backend");
    parameterUrl = `/audio/?session=${sessionId}`;
    fetch(parameterUrl,
        {
            method: "post",
            body: data,
            headers: {
                "X-CSRFToken": getCookie('csrftoken'),
                "TARGETSATZ": encodeURIComponent(textarea.val()),
            },
        }
    ).then(function (data) {
        data.text().then(text => {
            if (text != "Audio empfangen") {
                //aufnehmenErrorMessage.style.opacity = 1;
                //aufnehmenErrorMessage.innerHTML = text;
            }
        })
    })
}






