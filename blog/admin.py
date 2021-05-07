from django.contrib import admin
from .models import *

# Register your models here.
class BlogModelAdmin(admin.ModelAdmin):
    list_display = ('title','creat_time')#admin后台显示对应的字段
# admin.site.register([BlogTag,BlogCategory,BlogContent])
admin.site.register(BlogTag)
admin.site.register(BlogCategory)
admin.site.register(BlogContent, BlogModelAdmin)
