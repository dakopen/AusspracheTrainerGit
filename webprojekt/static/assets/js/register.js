$("#submit-register").prop("disabled", true);

$('#id_password1, #id_password2, #id_username').on('keyup', function () {
    checkAll();
    CheckPassword();
});


function checkAll(){
    if ($("#id_username").val() != "" && $('#username-already-exists').val() == ""){
        $("#submit-register").prop("disabled", false);
    }
}

function CheckPassword() {
// Fett markieren bei den Passworthinweisen, falls eine Sache nicht zutrifft.
// Javascript Passwort https://www.w3schools.com/howto/howto_js_password_validation.asp
}


$('#id_username').on('keyup', function () {
    checkUsername();
});


function checkUsername() {
    parameterUrl = `/benutzername/`;
    fetch(parameterUrl,
        {
            method: "post",
            body: $("#id_username").val(),
            headers: {
                "X-CSRFToken": getCookie('csrftoken'),
            },
        }
    ).then(function (data) {
        data.text().then(text => {
            if (text=="vergeben") {$('#username-already-exists').html("Dieser Benutzername ist vergeben. Bitte wähle einen anderen Benutzernamen.<br>");}
            else {$('#username-already-exists').html("");}
        })
    })
}







$('#id_password1, #id_password2').on('keyup', function () {
    if ($('#id_password1').val() == $('#id_password2').val()) {
        $('#password-matching').html('');
    } 
    else {
        if ($('#id_password2').val() != ""){
        $("#submit-register").prop("disabled", true);
        $('#password-matching').html('Die Passwörter stimmen nicht überein.').css('color', 'red');
        }
    }
});