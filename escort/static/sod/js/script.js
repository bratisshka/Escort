$(document).ready(function () {
    $(".button-collapse").sideNav();
    $('select').material_select();
    $('.modal').modal();
    $(".modal-test").click(function (e) {
        e.preventDefault();
        var load_url = $(this).attr('href');
        var modal_id = $(this).attr("modal");
        // $("#modal4").modal("open");
        $.ajax({
            url: load_url
        })
            .done(function (data) {
                // parsed_data = JSON.parse(data);
                // console.log(parsed_data.data);
                console.log(data.data);
                $("#out_file").text(data.data);
            });
        console.log(load_url);
        console.log(modal_id);
        $(modal_id).modal('open');
    });
    $(".href").click(function () {
        var href = $(this).attr('href');
        window.location.href = href;
    })

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
            setTimeout(function () {
                location.reload();
            }, 1000)
        }

    })
}

