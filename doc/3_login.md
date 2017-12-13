# 中间件与登录验证

## 中间件
#### 设置白名单
- 对于一些用户不需要登录就可以直接访问的网页，比如登录界面，我们在进行中间件验证的时候，应该将他们放在白名单中，用户即使没有登录，也可以访问白名单中的路径。
    - 白名单在setting.py中配置

```python
VALID_URLS = [
    'login',
    'admin.*',
]
```
    
#### 定义中间件    
- Django中要想实现中间件，需要自己定义一个中间件类，并继承自MiddlewareMixin类，在中间件中我们需要覆盖父类的`process_request`方法
        - MiddlewareMixin内部实现了`__init__`和`__call__`方法，前者不再陈述，对于`__call__`方法，简单的来说，就是当对象调用本身的时候，就会调用这个`__call__`方法，比如`a = A(); a()`

```python
# /room/middlewares/loginmd.py

from re import match

from django.conf import settings
from django.shortcuts import redirect


class MiddlewareMixin:
    def __init__(self, get_response=None):
        self.get_response = get_response
        super().__init__()

    def __call__(self, request):
        response = None
        if hasattr(self, 'process_request'):
            response = self.process_request(request)
        if not response:
            response = self.get_response(request)
        if hasattr(self, 'process_response'):
            response = self.process_response(request, response)
        return response


class LoginMiddleWare(MiddlewareMixin):
    """ 登陆验证中间件

    """

    def process_request(self, request):
        """ 在用户登陆前，对用户请求进行中间件验证
        Args:
            当前请求对象
        Return:
            None: 进入下一个中间件或视图函数
            rediect: 进入上一个中间件或wsgi，将响应返回给用户
        """

        current_url = request.path_info

        valid_urls = settings.VALID_URLS
        for url in valid_urls:
            regex = '^/room/{url}/$'.format(url=url)
            if match(pattern=regex, string=current_url):
                return None

        user_id = request.session.get('id')
        flag = True
        if not user_id:
            flag = False

        if not flag:
            return redirect('/room/login/')
        
```

#### 配置中间件
- 中间件定义完不要忘了去setting.py中配置中间件，不然写了也没用

```python
MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'room.middlewares.loginmd.LoginMiddleWare',                     # 登录验证中间件
]
```


## 登录页面及功能实现
1. 页面form表单渲染和后端表单数据验证使用的是form组件
2. 页面使用Ajax发送登录数据
3. 后端要完成三个验证（详情见需求分析）
4. 后端要返回验证结果对应的信息

#### form组件
- form组件需要设置三个字段
    - username
    - password
    - auto_login(BooleanField)
        - 用于用户下次直接自动登录

```python
from django.forms import Form
from django.forms import fields
from django.forms import widgets


class BaseInfoForm(Form):
    """ 基本用户信息form组件类

    """
    username = fields.CharField(required=True,
                                error_messages={'required': '用户名不能为空'},
                                widget=widgets.TextInput(attrs={'placeholder': '用户名',
                                                                'class': 'form-control',
                                                                'aria-describedby': "username"}))

    password = fields.CharField(required=True,
                                error_messages={'required': '密码不能为空'},
                                widget=widgets.PasswordInput(attrs={'placeholder': '密码',
                                                                    'class': 'form-control',
                                                                    'aria-describedby': "password"}))


class LoginForm(BaseInfoForm):
    """
        用于用户登陆的form组件类
    """
    auto_login = fields.BooleanField(required=False,
                                     widget=widgets.CheckboxInput(attrs={'value': 1}))

```


#### 前端页面

```html
{% load staticfiles %}
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <title>会议室预定系统</title>
    <link rel="stylesheet" href="{% static '/plugins/bootstrap/css/bootstrap.min.css' %}">
    <link rel="stylesheet" href="{% static '/css/login.css' %}">
</head>
<body>

<div class="container ">

    <div class="row my-style">
        <div class="col-md-4 col-md-offset-5">
            <p class="title">快来登陆吧</p>
        </div>
    </div>
    
    <div class="row">
        <div class="col-md-4 col-md-offset-4">
            <!-- form 表单 -->
            <form class="form-horizontal" novalidate>
                {% csrf_token %}
                <div class="form-group">
                    <label for="id_username" class="col-sm-4 control-label text-justify">用户名</label>
                    <div class="col-sm-8">
                        {{ form.username }}
                        <span id="username" class="help-block my-display"></span>
                    </div>
                </div>
                
                <div class="form-group">
                    <label for="id_password" class="col-sm-4 control-label text-justify">密码</label>
                    <div class="col-sm-8">
                        {{ form.password }}
                        <span id="password" class="help-block"></span>
                    </div>
                </div>


                <div class="form-group">
                    <div class="col-sm-offset-2 col-sm-10">
                        <div class="checkbox">
                            <label for="id_auto_login" class="col-sm-8 control-label">
                                {{ form.auto_login }}下次自动登录
                            </label>
                        </div>
                    </div>
                </div>
                
            </form>
            <div class="col-md-8 col-md-offset-5">
                    <button class="btn btn-default"  id="login" style="font-weight: bold;color: #904">登陆</button>
            </div>
        </div>
    </div>
</div>

<script src="{% static '/js/jquery-1.12.4.min.js' %}"></script>
<script src="{% static '/plugins/bootstrap/js/bootstrap.min.js' %}"></script>
<script src="{% static '/js/login.js' %}"></script>
</body>
</html>
```


#### Ajax
- Ajax发送的POST请求中，使用默认的请求体数据编码格式`application/www-form-urlencoded`，即服务端获取的数据为`username=xxx&password=xxx`的形式
    - 注意，如果你发送json类型的数据，就需要在Ajax中将数据使用`JSON.stringfy()`序列化，同时将制定编码格式为`application/json`，最最重要的是设置csrf-token值，对于如果发送的是json类型的数据，那么就不能将csrf-token设置在data中，而是应该设置在请求头中。

- Ajax业务逻辑
    - POST发送请求给服务器
    - 验证
        - 成功：跳转至预订会议室页面
        - 失败：渲染验证失败信息


```javascript
 $("#login").click(function () {
    // 发送Ajax请求

    $.ajax({
        url: "/room/login/",
        type: "post",
        data: {
            username: $('#id_username').val(),
            password: $('#id_password').val(),
            auto_login: $('#id_auto_login').val(),
            "csrfmiddlewaretoken": $("input:hidden").val()
        },
        success: function (data) {
            data = JSON.parse(data);
            
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
```


###### 视图函数
- 视图函数中的业务逻辑
    - 接收到客户端发送的请求
        - 是`GET`请求？
            - 在返回的render()函数中，完成login.html渲染，并将页面放在响应体中返回
        - 是`POST`请求？
            - 实例化LoginForm，开始form.is_valid()验证
                - 验证失败
                    - 组装数据结构data，将错误信息以及错误标识返回
                - 验证成功
                    - 进入数据库验证环节
                        - 验证失败：组装数据结构，添加错误信息至form.errors中，并返回data
                        - 验证成功：
                            1. 将用户信息保存至session中。
                                - 用户是否勾选了下次自动登录？
                                    - 是：设置session存在时间
                                    - 否：不做操作
                            2. 组装数据结构，将验证成功标识以及要跳转的目标路径封装到data中返回
                     
                           
```python
def login(request):
    """ 用户登录验证
    Args:
        request: 当前请求对象
    Return:
        HttpResponse: 包含验证结果的响应对象
    """

    if request.method == 'GET':
        form = LoginForm()
        return render(request, 'login.html', {"form": form})
    elif request.method == 'POST':
        form = LoginForm(data=request.POST)
        if form.is_valid():
            auto_login = form.cleaned_data.pop('auto_login')

            user = models.User.objects.filter(**form.cleaned_data)
            if user:
                request.session['username'] = user[0].username
                request.session['id'] = user[0].id

                if auto_login:
                    request.session.set_expiry(60*60*24*30)

                data = {
                    "success": True,
                    "location_href": '/room/'
                }
                return HttpResponse(dumps(data))
            else:
                form.add_error(field='password', error='用户名或密码错误')

                data = {
                     "success": False,
                     "form_errors": form.errors
                }
                return HttpResponse(dumps(data))
        else:
            data = {
                "success": False,
                "form_errors": form.errors
            }
            return HttpResponse(dumps(data))
```
















