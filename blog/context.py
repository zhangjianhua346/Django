#coding=utf-8
from django.db.models import Count
from blog.models import BlogContent
from django.db import connection


def getRightInfo(request):
    #获取分类信息
    categoryContext = BlogContent.objects.values('category__cname', 'category').annotate(c=Count('*')).order_by('-c') #返回的是quer_set对象
    # 'select category,count(*) as c from BlogContent GROUP by category order by c desc ' #返回的是元组

    #获取归档信息
    cursor = connection.cursor()
    # cursor.execute("select count(*) as c,creat_time from BlogContent GROUP by DATE_FORMAT(creat_time,'%Y-%m') order by c,creat_time desc")
    cursor.execute("select count(*) as c,data_time from BlogContent GROUP by data_time order by c,data_time desc")
    archiveInfoContext = cursor.fetchall()

    #获取近期文章
    recentBlogConext = BlogContent.objects.all().order_by('-creat_time')[:3]
    return {'categoryContext':categoryContext, 'recentBlogConext':recentBlogConext, 'archiveInfoContext':archiveInfoContext}