#coding=utf-8
from django.http import HttpResponse


def index_views(request):
    return HttpResponse("hello word!")




