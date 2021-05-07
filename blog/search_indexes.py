#coding=utf-8

from haystack import indexes
from blog.models import *  #引入应用包的模型类

#注意格式（模型类名+index）
class BlogContentIndex(indexes.SearchIndex,indexes.Indexable):
    text = indexes.CharField(document=True, use_template=True)

    #给模型类中的字段设置索引
    title = indexes.NgramField(model_attr='title')
    content = indexes.NgramField(model_attr='content')

    def get_model(self):#重写index索引方法
        return BlogContent
    def index_queryset(self, using=None):
        return self.get_model().objects.order_by('-creat_time')#返回模型类查询的结果并以某个字段排序
