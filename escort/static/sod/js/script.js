$(document).ready(function () {
    $(".button-collapse").sideNav();
    $('select').material_select();
    $('.modal').modal();


});

function csrfSafeMethod(method) {
    // these HTTP methods do not require CSRF protection
    return (/^(GET|HEAD|OPTIONS|TRACE)$/.test(method));
}

function clean_module_subdir(module_id, type) {
    var csrftoken = jQuery("[name=csrfmiddlewaretoken]").val();
    $.ajax({
        type: "POST",
        url: "/sod/module/" + module_id + "/clean_" + type + "/",
        beforeSend: function (xhr, settings) {
            if (!csrfSafeMethod(settings.type) && !this.crossDomain) {
                xhr.setRequestHeader("X-CSRFToken", csrftoken);
            }
        },
        success: function () {
            Materialize.toast('Очищено!', 4000);
        }

    })
}

