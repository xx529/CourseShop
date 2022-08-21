from django.utils.deprecation import MiddlewareMixin

class MyMiddleware(MiddlewareMixin):

    # 初始化中间件
    def __init__(self, get_response=None):
        super().__init__(get_response)
        print('init_mymiddleware')

    # 请求中间件
    def process_request(self, request):
        request.context = {}
        if 'session_user' in request.session.keys():
            request.context['session_user'] = request.session['session_user']


    # 响应中间件
    def process_response(self, request, response):
        return response