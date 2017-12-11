 $("#login").click(function () {
    // 发送Ajax请求

     console.log($('#id_username').val());
     console.log($('#id_password').val());
    $.ajax({
        url: "/room/login/",
        type: "post",
        data: {
            username: $('#id_username').val(),
            password: $('#id_password').val(),
            "csrfmiddlewaretoken": $("input:hidden").val()
        },
        success: function (data) {
            data = JSON.parse(data);
            console.log(data);
            // 用户登陆成功
            if (data["success"]) {
                    window.location.href = data["location_href"];
            }

            // 用户登陆失败，渲染错误信息
            if (data["form_errors"]) {

                for (var key in data["form_errors"]) {
                    $("#" + key).text(data["form_errors"][key]);
                    $("#" + key).parent().parent().addClass('has-error');
                }
            }
        }
    });
 });



