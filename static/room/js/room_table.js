/*
    初始化日历插件并绑定时间
 */
$('#datetimepicker').datetimepicker({
    format: 'yyyy/mm/dd',
    language: 'zh-CN',
    minView: "month",
    autoclose: true,
    startDate: new Date(),
    todayBtn: true
}).on('changeDate', function () {
    var new_date = $(this).val();
    var form = $("form");
    form.attr('action', '/room/' + new_date);
    console.log(form);
    console.log(form[0]);
    form[0].submit();
});

/*
    使用Ajax提交"撤销曾经订单"请求
 */
$(".order").click(function () {
    var current_user = $("#username").val();
    var selected_val = $(this).text();
    if (selected_val) {
        if (selected_val !== current_user) {
            // 如果点击的是别人预定的, 后端也要验证
            alert('该会议室已被' + selected_val + '预订！')
        } else {
            // 如果再次点击之前自己预定的order，会清除
            var that = $(this);
            // 发送ajax清除这个预订, 后端需要验证这个order是不是这个人预订的，有可能伪造请求删除其他人的
            $.ajax({
                url: '/room/checkout/' + $(this).attr('order_id'),
                type: 'get',
                success: function (data) {
                    data = JSON.parse(data);
                    if (data['success']){
                        alert('取消预订成功');
                        that.removeClass('has_ordered');
                        that.text('');
                    }else {
                        alert('操作失败')
                    }
                }
            });
        }
    }
    else {
        // 如果点击的是尚未被预订过的
        $(this).toggleClass('has_selected');
    }
});

/*
    使用Ajax提交指定日期的预定
 */
$("#submit").click(function () {
    var data = {};

    $.each($(".room"), function () {
        data['schedule_date'] = $("#datetimepicker").val();
        var order_list = data[$(this).attr('id')] = [];
        // 获取本次预订的
        $.each($(this).find('.has_selected'), function () {
            order_list.push($(this).attr('id'));
        });
    });
    $.ajax({
        url: '/room/commit_choice/',
        data: JSON.stringify(data),
        type: 'post',
        headers: {
            'X-CSRFToken': $("[name='csrfmiddlewaretoken']").val()
        },
        contentType: 'application/json',
        success: function (data) {
            data = JSON.parse(data);
            if (data['success']){
                alert(data['message']);
                window.location.href = '/room/'
            }else {
                alert('预订失败')
            }
        }
    })
});


