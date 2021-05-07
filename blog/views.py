import math
from django.http import HttpResponse
from django.shortcuts import render

# Create your views here.
from blog.models import *
from django.core.paginator import Paginator

def home_page(request, num=1):
    """博客首页"""
    num = num if num else 1
    num = int(num)
    #获取所有的博客信息
    contentList =BlogContent.objects.all().order_by('-creat_time')
    pageNumList,prepageList = paginate_obj(contentList=contentList, pagesize=1, pagenum=num)
    return render(request,'blog_home_page.html',{'contentList':prepageList, 'pageList':pageNumList, 'currentNum':num})

def paginate_obj(contentList, pagesize=1, pagenum=1):
    """返回分页对象"""
    # 创建分页器对象
    pageObj = Paginator(contentList, pagesize)
    # 获取当前页数据
    prepageList = pageObj.page(pagenum)

    # 生成页码数列表
    # 每页开始页码
    begin = (pagenum - int(math.ceil(10.0 / 2)))
    if begin < 1:
        begin = 1
    # 每页结束页码
    end = begin + 9
    if end > pageObj.num_pages:
        end = pageObj.num_pages
    if end <= 10:
        begin = 1
    else:
        begin = end - 9
    pageNumList = range(begin, end + 1)
    return pageNumList,prepageList




def content_detail(request,contentId):
    """查看博客详情"""
    contentId = int(contentId)
    contentDetail =BlogContent.objects.get(id=contentId)
    return render(request,'blog_detail.html', {'contentDetail':contentDetail})


def query_blog_by_categroyid(request, categroyid):
    """根据博客分类查询所有的博客"""
    categoryList = BlogContent.objects.filter(category_id=categroyid)
    return render(request, 'blog_article.html', {'categoryList':categoryList})

def query_blog_by_archive_time(request, year, month, day):
    """查看归档博客文章按日期"""
    archiveList = BlogContent.objects.filter(creat_time__year=year,creat_time__month=month,creat_time__day=day)
    return render(request, 'blog_article.html', {'categoryList':archiveList})


from django.core.cache import caches
#获取缓存对象
cache = caches['default']
def cache_view(func):
    """手动缓存"""
    def _wrapper(request, *args, **kwargs):
        data = cache.get(request.path)
        if data:
            print('读取缓存数据')
            return HttpResponse(data)
        print('读取数据库数据')
        response = func(request, *args, **kwargs)
        print('进行缓存数据')
        cache.set(request.path,response.content)
        return response
    return _wrapper
@cache_view
def test_cache(request):
    """读取数据库数据"""
    return HttpResponse('111')
