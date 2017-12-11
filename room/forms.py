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
    pass