from re import match

from django.conf import settings
from django.shortcuts import redirect

from room import models

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