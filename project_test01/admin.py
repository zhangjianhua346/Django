from django.contrib import admin
from .models import *
#Register your models here.
#在后台中可以看到表film ，http://127.0.0.1:8000/admin/
admin.site.register([Film,C_Class,C_Student,User,Student,Card,File_Student])

#可以修改admin后台显示布局
# class BlogAdmin(admin.ModelAdmin):
#     list_display = ('title','author','publish')