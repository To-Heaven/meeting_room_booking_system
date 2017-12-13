# 预订主页面设计


## 页面渲染（表格与日历插件）

#### 日历插件
- 日历插件使用的是BootStrap提供日历插件，再使用之前，需要在主页面上导入包及其依赖

```html
    <link rel="stylesheet" href="{% static '/plugins/bootstrap/css/bootstrap.min.css' %}">
    <link rel="stylesheet" href="{% static '/css/room_table.css' %}">
    <link rel="stylesheet" href="{% static '/plugins/datetimepicker/bootstrap-datetimepicker.min.css' %}">
    
    <!-- 中间忽略 -->
    
    <script src="{% static '/js/jquery-1.12.4.min.js' %}"></script>
    <script src="{% static '/plugins/bootstrap/js/bootstrap.min.js' %}"></script>
    <script src="{% static '/plugins/datetimepicker/bootstrap-datetimepicker.min.js' %}"></script>
    <script src="{% static '/plugins/datetimepicker/bootstrap-datetimepicker.zh-CN.js' %}"></script>
    <script src="{% static '/js/room_table.js' %}"></script>
```

- 在`table.html`中，需要一个`input`输入框，由于本项目中使用form标签的submit方法提交表单中的日期来实现查询的功能，所以在这儿将input框放在form表单中

```html
            <form>
                {% csrf_token %}
                <!-- 日历插件 -->
                <div class="col-md-2 timer">
                    <input type="text" readonly value="{{ today }}" id="datetimepicker" class="form-control">
                </div>
            </form>
```

- 在`table.js`中，来实现日历插件的功能
    - 使用datetimepicker对象的changeDate事件可以跟踪日历插件中日期的变化，当日期变化的时候执行事件回调函数中的Ajax程序
    - 细节
        1. 这里将日期的格式修改成带有斜杠的形式，是为了方便url的拼接，后端url映射中，会解析类似"/room/2015/12/24/"的路径，对应的视图函数会从数据库中获取指定日期的所有预订记录，组装成指定数据结构后返回被渲染的页面

```javascript
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
```

#### 表格渲染
###### 表格要实现的功能
1. 渲染已有预订记录
    - 已经被预订的时间段代表的单元格一定得和其他单元格能够区分开，因此需要有属性用来标识，这个属性可以是class，也可以是我们自定义的属性。
    - 用户之前预订的记录要与其他用户预订的记录区分开，因为我们要实现用户撤销预订的功能
2. 渲染表格
    - 表格的13个时间段，每一个时间段都应该与其他时间段之间能够区分开，这样在用户提交预订的时候，我们可以通过提交的数据来确定用户要定义的是哪一个时间段以及是哪一个会议室
3. 

###### 表格渲染有两种方式（数据结构一定要为功能实现而设计）
1. 使用Django内置的模板渲染，这种方式需要在后端生成一个能够实现前端功能的数据结构
    - 设计的数据结构如下， 如果设计成这种结构，**标签的属性就需要我们在模板渲染中指定，优点是快速方便**

```python

{
    room_obj1: {
        period1: order_obj1,
        period2: order_obj2,
    }

    room_obj2: {
        period2: order_obj3,
        period4: order_obj4,
    }
}

# 举例
{
    <MeetingRoom: 1001>: {
        1: <Order: date:2017-12-21 period:1 room：1001>, 
        6: <Order: date:2017-12-21 period:6 room：1001>}, 
    <MeetingRoom: 1301>: {}
}
```


2. 页面加载结束后，使用Ajax发送请求获取特定数据结构的数据，这个数据也得满足能够实现前端功能
    - 设计的数据结构如下，如果设计成这种结构，**标签的属性就需要我们在数据结构中指定，优点是功能实现上更丰富和灵活**
        
```python
[
    [{"text": room_name, "attr":{"room_id":room_id}}, {"text":""}, {}]
]

```

###### 模板及视图函数

```html
<table class="mytable table table-bordered text-center">
                <thead>
                <tr>
                    <th>会议室</th>
                    <th>8:00</th>
                    <th>9:00</th>
                    <th>10:00</th>
                    <th>11:00</th>
                    <th>12:00</th>
                    <th>13:00</th>
                    <th>14:00</th>
                    <th>15:00</th>
                    <th>16:00</th>
                    <th>17:00</th>
                    <th>18:00</th>
                    <th>19:00</th>
                    <th>20:00</th>
                </tr>
                </thead>
                <tbody>
                {% for room, item in result_dict.items %}
                    <tr id="{{ room.id }}" class="room">
                        <td>{{ room.title }}(最大容纳{{ room.number_of_people }}人)</td>
                        {% for period in period_list %}
                            {% if period.0 in item.keys %}
                                {% for k, v in item.items %}
                                    {% if period.0 == k %}
                                        <td id="{{ period.0 }}" class="has_ordered order"
                                            order_id="{{ v.id }}">{{ v.user }}</td>
                                    {% endif %}
                                {% endfor %}
                            {% else %}
                                <td id="{{ period.0 }}" class="order"></td>
                            {% endif %}
                        {% endfor %}
                    </tr>
                {% endfor %}
                </tbody>
            </table>
```

- 用户登录进入主页面时，默认是当前日期对应的预订界面，当点击日历获取其他日期的预订情况时，后端处理返回的应该是相同结构的数据，这里将数据处理的过程封装到一个函数中

```python
def get_data(rooms, orders):
    """ 生成渲染预订页面的数据结构
    Args:
        rooms: queryset, 会议室记录对象组成的queryset对象
        orders: queryset, 制定日期订单记录对象组成的queryset对象
    Return:
        result_dict: dict, 存放了渲染页面数据的字典
    """

    result_dict = {}
    for room in rooms:
        result_dict[room] = {}
        for order in orders:
            if order.room == room:
                result_dict[room][order.period] = order
    return result_dict


def table_orders(request):
    """ 处理主页面GET请求，并渲染模板的视图函数
    Args:
        request: 当前请求对象
    Return:
        HttpResponse: 包含主页面数据的响应对象
    """

    if request.method == 'GET':
        today = datetime.datetime.today()
        orders = models.Order.objects.filter(schedule_date=today)
        rooms = models.MeetingRoom.objects.all()

        result_dict = get_data(rooms, orders)
        return render(request, 'room_table.html', {
            "today": today.strftime('%Y-%m-%d'),
            "period_list": models.Order.period_list,
            "result_dict": result_dict
        })


def table_change(request, year=None, month=None, day=None):
    """ 渲染指定日期预订页面的视图函数
    Args:
        request: 当前请求对象
        year： 指定的年份
        month： 指定月份
        day： 指定日期
    Return:
        HttpResponse: 包含页面数据的响应对象
    """

    select_time = datetime.datetime(year=year, month=month, day=day)
    orders = models.Order.objects.filter(schedule_date=select_time)
    rooms = models.MeetingRoom.objects.all()

    result_dict = get_data(rooms, orders)
    return render(request, 'room_table.html', {
        "today": select_time.strftime('%Y-%m-%d'),
        "period_list": models.Order.period_list,
        "result_dict": result_dict
    })
```

#### 实现撤销预订
- 撤销预订是通过ajax请求来实现的，当用户点击一个单元格时，会触发以下程序依次执行
    1. 首先在js文件中获取当前登录用户的用户名，单元格中的预订人的姓名，用户信息可以再渲染模板的时候存储在隐藏的标签中，也可以存放在cookie中，使用jquery.cookie来存取用户信息。
        - 如果得到的两个姓名不相同，说明当前单元格上的预订信息是其他用户预订的，肯定不能让当前用户撤销，这个验证的过程一定要在后端也进行验证，因为用户完全可以修改页面信息之后再出发ajax请求，前端这个设置是为了避免用户频繁的无效撤销ajax请求
        - 如果得到的两个姓名相同，说明当前单元格上的预订信息是当前用户本人预订的，当然也需要在后端验证，这个也可以伪造。
    2. 后端根据提交的预订记录id和当前登录的用户进行验证，
        - 如果在数据库中能够匹配到一条记录，那么说明验证成功，后端就会从数据库中删除这条预订记录，并返回成功的标识信息
        - 如果在数据库中无法匹配到这条记录，那么说明验证失败，后端就会返回失败的标识信息
    3. 前端ajax接收到响应数据之后，会对标识信息data中的“suceess”键进行判断
        - 如果success为true，那么就在页面上清空着一条预订记录，同时清空样式
        - 如果success为false，那么就弹出警告框

- ajax请求如下

```javascript
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
```

- 对应后端视图函数验证过程及删除预订记录

```python
def checkout(request, order_id=None):
    """ 验证用户撤销操作，如果验证成功，就撤销用户预订，对应的从数据库中删除一条记录
    Args:
        request: 当前请求对象
        order_id: 要撤销的预订记录的id
    Return:
        HttpResponse: 响应信息
    """
    
    user_id = request.session.get('id')
    order = models.Order.objects.filter(user__id=user_id, id=order_id)
    if not order:
        data = {"success": False}
        return HttpResponse(dumps(data))
    else:
        order.delete()
        data = {"success": True}
        return HttpResponse(dumps(data))
```
        
   
#### 实现提交预订
- 前端中，用户每点击一个单元格，都会出发这个单元格对应的点击事件，该单元格会被添加样式并且添加一个类"has_selected"，当用户点击提交按钮的时候，出发提交按钮的点击事件，程序会从页面上收集当前用户的预订信息，并组装成方便后端解析的数据结构，以json数据发送给后端

- 数据结构

```
{
    schedule_date: 提交日期,
    room_id1: [order_id1, order_id2, ...],
    room_id2: [order_id1, order_id2, ...]
}
```

- 细节注意
    - 由于这次提交的数据全部按照json格式并以POST请求发送给后端，因此我们要提供的csrf-token值就不能放在data中，因为csrf-token值如果也被序列化了，那么Dajango的中间件csrfmiddlewaretoken验证时就无法解析我们提交的数据，因此我们需要在请求头中设置csrf-token数据
    - 还有一种方式发送数据就可以将csrf-token数据放在data中，我们只需要将data中的一部分数据序列化，发送的请求体中的编码仍然是用默认的编码`application/www-form-urlencoded`

```
{
    schedule_date: 提交日期,
    csrfmiddlewaretoken: $("[name=csrfmiddlewaretiken]").val(),
    order_data: JSON.stringfy({
    room_id1: [order_id1, order_id2, ...],
    room_id2: [order_id1, order_id2, ...]
    }),
}

```

- ajax代码实现

```javascript
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
```

- 后端视图函数数据处理


```python
def commit_choice(request):
    """ 处理用户提交的预订信息
    Args:
        request: 当前请求对象
    Return:
        HttpResponse: 处理成功后的响应信息
    """
    
    data = loads(request.body.decode('utf-8'))
    user_id = request.session.get('id')
    schedule_date = data['schedule_date']
    del data['schedule_date']                               # 清除创建order对象时不需要的字段

    order_list = []
    for room_id, periods in data.items():
        for period in periods:
            order_list.append(models.Order(
                period=period,
                room_id=room_id,
                user_id=user_id,
                schedule_date=schedule_date
            ))
    models.Order.objects.bulk_create(order_list)            # 批量插入
    response_data = {"success": True, "message": '预订成功'}
    return HttpResponse(dumps(response_data))
```




































    

