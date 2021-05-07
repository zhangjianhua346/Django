from django.db import models
from ckeditor_uploader.fields import RichTextUploadingField

# Create your models here.

class BlogCategory(models.Model):
    """博客分类表"""
    cname = models.CharField(max_length=30,unique=True,verbose_name=u'分类名')
    class Meta:
        db_table = 'BlogCategory'
        verbose_name_plural = u'类别'
    def __str__(self):
        return u'BlogCategory:%s'%self.cname

class BlogTag(models.Model):
    """博客标签表"""
    tname = models.CharField(max_length=30,unique=True)
    class Meta:
        db_table = u'BlogTag'
    def __str__(self):
        return u'BlogTag:%s' % self.tname

class BlogContent(models.Model):
    title = models.CharField(max_length=300,unique=True)
    desc = models.CharField(max_length=100)
    # content = models.TextField()
    content = RichTextUploadingField() #富文本编辑器
    creat_time = models.DateTimeField(auto_now_add=True)
    data_time = models.DateField(auto_now_add=True)
    last_update_time = models.DateTimeField(auto_now=True)
    category = models.ForeignKey(BlogCategory,on_delete=models.CASCADE)
    tag = models.ManyToManyField(BlogTag)
    class Meta:
        db_table = u'BlogContent'
    def __str__(self):
        return u'BlogContent:%s' % self.title