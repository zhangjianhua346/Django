#coding=utf-8
from django.utils.deprecation import MiddlewareMixin

class Mid1(MiddlewareMixin):
    def process_request(self,request):
        print("中间件1")

    # def process_view(self,request):
    #     print('中间件view1')

    def process_response(self,request,response):
        print("中间件响应1")
        return response


class Mid2(MiddlewareMixin):
    def process_request(self, request):
        print("中间件2")

    def process_response(self, request, response):
        print("中间件响应2")
        return response


class Mid3(MiddlewareMixin):
    def process_request(self, request):
        print("中间件3")

    def process_response(self, request, response):
        print("中间件响应3")
        return response