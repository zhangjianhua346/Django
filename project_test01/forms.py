#coding=utf-8

from django import  forms
class LoginFormsClass(forms.Form):
    """定义一个表单类--->对应画HTML的表单"""
    sname = forms.CharField(max_length=32,label=u'姓名')
    password = forms.CharField(max_length=16,label=u'密码',widget=forms.PasswordInput)#widget=forms.PasswordInput --密码框

#查询用forms.Form，插入数据库用forms.ModelForm--提供了save方法
from project_test01.models import ModelStudentForms, ModelClassForms
class StudentForms(forms.ModelForm):
    pwd = forms.CharField(widget=forms.PasswordInput,max_length=16,label='原密码')#方法一：增加字段 #lable==模型类中的verbose_name
    confirm_pwd = forms.CharField(widget=forms.PasswordInput,max_length=16,label='确认密码')
    class Meta:
        model = ModelStudentForms
        fields = ('sname',)#方法二：指定显示出models类的字段
    def checkpwd(self):#定义表单类校验函数
        """校验原密码跟确认密码是否一致"""
        data = self.cleaned_data
        if data['pwd'] != data['confirm_pwd']:
            self.errors['confirm_pwd'] = ['密码不一致']#错误提示信息给到html可以是多个，所以是列表
            return False
        return data['pwd']

class ClassForms(forms.ModelForm):
    class Meta:
        model = ModelClassForms
        fields = ('cname',)