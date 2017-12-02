$(document).ready(function () {
    var subtask_count = 0;
    $('.collapsible').collapsible();
    $("#add_subtask").click(function () {
        $.ajax({
            data: {
                'count': subtask_count
            },
            url: '/ocs/add_subtask',
            success: function (data) {
                var cont = document.createElement("div");
                cont.setAttribute("id", "subtask" + subtask_count.toString());
                $("#subtasks").append(cont);
                $("#subtask" + subtask_count.toString()).html(data);
                $('select').material_select();
                subtask_count += 1;
            }
        })
    });
    $("#submit_form").click(function (e) {
        e.preventDefault();
        var serial_form = $("#task_form").serialize();
        console.log(serial_form);
        if ($("#subtask0").length) {
            serial_form += "&subtasks=1"
        }
        $.ajax({
            data: serial_form,
            type: "POST",
            url: '/ocs/add_task/',
            success: function (data) {
                console.log(data);
                $(".subtask_form").each(function (index, element) {
                    var subtask_serial = $(this).serialize();
                    subtask_serial += "&task=" + data;
                    $.ajax({
                        data: subtask_serial,
                        type: "POST",
                        url: '/ocs/add_subtask/',
                        success: function (data) {
                            console.log("ZBZ")
                        },
                        error: function (data) {
                            console.log(data);
                            // TODO что-то с этим надо делать, например, удалять родительский таск
                        }
                    })
                });
                window.location = '/ocs/show_task/' + data;
            },
            error: function (data) {
                location.reload()
            }

        });
        //  $.post( '/ocs/add_task/', serial_form, function (data) {
        //      console.log(data);
        //      // Добавление подазач
        //      window.location = '/ocs/show_task/' + data.toString();
        //  });
        console.log("kek");
    });
});

