import math
import os

from django.contrib.auth import authenticate, login
from django.http import HttpResponse, HttpResponseRedirect, Http404, FileResponse, JsonResponse
from django.shortcuts import render, redirect

# Create your views here.
from django.template import Template, context, loader, Context, RequestContext
from django.urls import reverse
from django.views.decorators.csrf import csrf_protect, csrf_exempt

from project_test01.models import *

def test(request):
    """页面显示hello word!"""
    return HttpResponse("hello word!")


# def login(request):
#     """渲染登录首页"""
#     return render(request,'login.html')


def login_operation(request):
    """渲染登录首页且处理登录功能"""
    #接收请求参数
    uname = request.POST.get("uname",'')#没有就赋值''
    pwd = request.POST.get("pwd")
    #判断
    if uname =='zhangsan' and pwd =='123':
        return HttpResponse('登录成功！')
    return HttpResponse('登录失败！')


def register_index(request):
    return render(request, 'register.html')

def register(request):
    uname = request.POST.get("uname", '')
    pwd = request.POST.get("pwd")
    try:
        if uname and pwd:  # 非空判断
            # 创建模型对象
            user = User(sname=uname, spwd=pwd)
            # 插入数据库
            user.save()
            return HttpResponse('注册成功！')
    except Exception as e:
        return HttpResponse('注册失败！')

def register1(request):
    """注册到数据库，一个方法包含了首页展示和注册功能"""
    # 获取前端请求方式
    method = request.method
    if method == 'POST':
        return render(request, 'register.html')
    else:
        uname = request.POST.get("uname", '')
        pwd = request.POST.get("pwd")
        try:
            if uname and pwd:  # 非空判断
                # 创建模型对象
                user = User(sname=uname, spwd=pwd)
                #User.objects.create(sname=uname, spwd=pwd)
                # 插入数据库
                user.save()
                return HttpResponse('注册成功！')
        except Exception as e:
            return HttpResponse('注册失败！')


def user_query(request):
    #查询数据库数据
    all_user_data = User.objects.all() #返回的是列表
    return render(request,'user_query.html',{'all_user_data':all_user_data})

def pager(page_num,page_size=20):
    #接收当前页码数
    page_num = int(page_num)
    #获取总记录数
    total_records =Film.objects.count()
    #总页数 ceil向上取整
    import math
    total_pages = int(math.ceil(total_records*1.0/page_size))
    #判断是否越界
    if page_num < 1:
        page_num = 1
    elif page_num > total_pages:
        page_num = total_pages
    #计算每页显示的记录
    film_records = Film.objects.all()[((page_num - 1) * page_size): (page_num * page_size)]
    return film_records,page_num

def film_pager(request):
    """电影列表自定义分页展示"""
    #接收页面请求参数page_size，page_num 字符串
    page_num = request.GET.get('page_num','1')
    #处理分页请求
    film_records,page_num = pager(page_num)
    #上下页的页码
    pre_page_num = page_num -1
    next_page_num = page_num +1
    return render(request,'film_list.html',{'film_list':film_records,'pre_page_num':pre_page_num,'page_num':page_num,'next_page_num':next_page_num})


def native_pager_film(request):
    """自带原生分页器"""
    from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
    # 接收当前页码数
    page_num = request.GET.get('num', '1')
    page_num = int(page_num)
    print('页数为：{}'.format(page_num))
    page_size = 1
    # 查询出所有数据--获取的是对象列表
    films = Film.objects.all()
    # 创建分页器对象-->总的分页器
    total_pages_object = Paginator(films, page_size)
    #总页数
    total_pages = total_pages_object.num_pages
    try:
        curr_page_records = total_pages_object.page(page_num)#获取当前页的数据
    except PageNotAnInteger:  # 小于1显示第一页
        curr_page_records = total_pages_object.page(1)
    except EmptyPage:  # 超出显示最后一页
        curr_page_records = total_pages_object.page(total_pages)
    #每页起始页码
    begin_pages = (page_num-int(math.ceil(10.0/2)))
    # 每页的结束页码
    end_pages = begin_pages + 9
    if begin_pages < 1:
        begin_pages = 1
    # else:
    #     if end_pages > total_pages:
    #         end_pages = total_pages
    if end_pages <= 10:
        begin_pages = 1
    else:
        begin_pages = end_pages - 9
    if end_pages>total_pages:
        end_pages = total_pages
    page_list = range(begin_pages,end_pages+1)
    return render(request,'native_film_list.html',
                  {'film_list':curr_page_records,'total_pages_object':total_pages_object,'page_list':page_list,'page_num':page_num})


def student_pro_register(request):
    """班级的学生在页面选择注册多课程"""
    if request.method=='GET':
        return render(request,'student_pro_register.html')
    else:
        #接收请求参数
        sname = request.POST.get('sname')
        cname = request.POST.get('cname')
        cournames = request.POST.getlist('coursename','')#接收的是列表
        #将数据注册到数据库
        flag = registerStu(sname,cname,*cournames)
        if flag:
            return HttpResponse("注册成功！")
        else:
            return HttpResponse("注册失败！")


def student_pro_register_showall(request):
    """显示所有的班级学生的信息列表"""
    cls = SClass.objects.all()
    return render(request,'student_pro_register_showall.html',{'cls':cls})


def getstu_detail(request):
    """显示学生选课的详情"""
    #获取班级信息
    cno = request.GET.get('cno','')
    cno = int(cno)
    #根据班级查询学生信息
    stus = SClass.objects.get(c_no=cno).sstudent_set.all()

    return render(request,'stu_detail.html',{'stus':stus})


def test_url(request, num):
    """测试url传参的方法,关键字传参"""
    return HttpResponse(num)


def test_url2(request,year, month ,day):
    """"
    测试url传参的方法,关键字传参
    """
    return  HttpResponse("%s-%s-%s"%(year, month ,day))


def test_url3(request,year, month ,day):
    """"
    测试url传参的方法, 位置传参
    """
    return HttpResponse("%s-%s-%s"%(year, month, day))


def test_url4(request, year, month ,uname):
    """"
    测试url传参的方法, 位置传参
    """
    return HttpResponse("%s-%s-%s" % (year, month, uname))


def reverse_url_index(request):
    return render(request,'reverse_url.html',{'n':16})
def reverse_url(request,num):
    """"
     测试url传参的方法, 作用于子路由
    """
    return HttpResponse("测试逆向路由从html中的q匹配url再匹配views的函数+{}".format(num))


def reverse_redirect_urls(request):
    """测试url传参的方法,重定向"""
    return HttpResponseRedirect(reverse('q',args=(66,)))


def inculde(request):
    """测试url传参的方法,作用于根路由"""
    return HttpResponse("作用于根路由")



def index(request):
    return render(request,'http.html')
def test_http_request(request):
    """http对象"""
    method = request.method
    body = request.body
    name = request.POST.get('uname')
    # response = HttpResponse('hello')
    # response.__setitem__('Server','wsg')#修改响应中的host
    response = HttpResponse('<h1 style="color:red">hello</h1>')
    return response


def file_upload(request):
    """图片上传至本地"""
    if request.method=='GET':
        return render(request,'file_upload.html')
    elif request.method=='POST':
        #获取请求参数
        uname = request.POST.get('uname','')
        photo = request.FILES.get('photo','')
        if not os.path.exists('media'):
            os.makedirs('media')
        with open(os.path.join(os.getcwd(),'media',photo.name),'wb') as fw:
            # fw.write(photo.read())
            """分块读取。速度快"""
            for chunk in photo.chunks():
                fw.write(chunk)
        return HttpResponse('上传成功')
    else:
        return HttpResponse('上传文件服务器异常')


def file_upload_db(request):
    """图片上传至数据库"""
    if request.method == 'GET':
        return render(request, 'file_upload_db.html')
    elif request.method == 'POST':
        # 获取请求参数
        uname = request.POST.get('uname', '')
        photo = request.FILES.get('photo', '')
        #入库操作
        File_Student.objects.create(sname=uname,photo=photo)
        return HttpResponse('图片上传至数据库成功')


def show_all_photo(request):
    """显示图片"""
    all_photos =File_Student.objects.all()
    return render(request, 'show_all_photo.html', {'all_photos':all_photos})


def photo_download(request):
    """下载图片"""
    #获取请求参数
    photo = request.GET.get('photo','')
    #获取图片文件名
    filename = photo[photo.rindex('/')+1:]
    #开启一个流
    path = os.path.join(os.getcwd(), 'media', photo.replace('/','\\'))
    with open(path,'rb') as fr:
        response = HttpResponse(fr.read())
        response['content-type'] = 'image/png'#修改响应
        response['content-Disposition']='attachment;filename='+filename
    return  response



def redirect_befor(request):
    """重定向之前页面"""
    # return HttpResponseRedirect('/redirect/redirect_after/') #--->302
    # return redirect('/redirect/redirect_after/',permanent=True) #-->301永久重定向
    #通过改响应信息
    response = HttpResponse()
    response.status_code = 302
    response.setdefault('location','/redirect/redirect_after/')
    # response['status_code'] =302
    # response.__setitem__('location','/redirect/redirect_after/')
    return response

def redirect_after(request):
    """重定向之后页面"""
    return HttpResponse('被重定向了')


def error_page_custom(request):
    """定制错误页面,只要报404就会去找到templates中的404.html"""
    pass

import datetime
def cookie(request):
    #创建响应对象
    response = HttpResponse()
    #将数据存储在cookie中,默认保存在浏览器缓存中关闭浏览器就消失，持久会得加上max_age,cookie保存项目哪个路径加上path,
    # 失效时间加expire,domain指定哪个域名下cookie有效(None当前域名下全部有效)，加盐salt(set_cookie是不能加salt)
    response.set_signed_cookie('uname', 'zhangsan', salt='xxxsign', max_age=24*60*60, path='/', expires=datetime.datetime.today()+datetime.timedelta(days=2))
    # #删除cookie
    # response.delete_cookie('uname', path='/')
    # response['max_age'] = -1
    return response

def get_cookie(request):
    #uname = request.COOKIES.get('uname')
    if request.COOKIES.has_key('uname'):#python3没有has_key方法
        uname = request.get_signed_cookie('uname', salt='xxxsign')
        return HttpResponse(uname)
    else:
        return HttpResponse('当前cookie信息不存在')


def set_cookie_login(request):
    """三天免登陆"""
    if request.method=='GET':
        #判断客户端是否存在cookie信息
        if 'login_key' not in request.COOKIES:
            return render(request, 'set_cookie_login.html')
        else:
            uname_pwd = request.COOKIES.get('login_key','')
            name, password  = uname_pwd.split(',')
            return render(request, 'set_cookie_login.html', {'name':name, 'password':password})
    else:
        #接收接口参数
        uname = request.POST.get('uname','')
        pwd = request.POST.get('pwd','')
        flag = request.POST.get('flag','')
        #判断是否登录成功
        response = HttpResponse()
        if uname=='zhangsan' and pwd =='123':
            response.content = '登录成功！' #response = HttpResponse('登录成功！')
            if flag == '1':#记住密码
                response.set_cookie('login_key', uname + ',' + pwd, path='/', max_age=24 * 60 * 60 * 3)
                return response
            else:
                return response
        else:
            #登录失败，清空cookie
            response.delete_cookie('login_key',path='/')
            response.content = '登录失败！'
            return  response


def session(request):
    #在session中存放数据
    request.session['uname'] = 'zhangsan'#存放在sessionStore对象本身
    #设置session有效时间(整数：秒，0,：关闭浏览器过期，日期：指定日期过期，none：默认)
    request.session.set_expiry(24*60*60*3)
    #删除session数据
    # del request.session['uname'](只是删除这个对象session信息)
    # request.session.clear()#清空所有的session对象的session_id
    # request.session.flush()#清空所有的session包括数据库的当前这个session_key
    return HttpResponse('设置成功')

def get_session(request):
    """获取session"""
    uname = request.session['uname']
    # print(request.session.session_key) #-->cookie中的session_id
    return HttpResponse(uname)

import jsonpickle
def usercenter(request):
    """用户中心"""
    uname = request.session['login']
    user = request.session['login_']
    user_object = jsonpickle.loads(user)#将普通字符串反序列化成对象
    return render(request,'usercenter.html',{'uname':uname,'user_object':user_object})
def set_session_login(request):
    if request.method=='GET':
        return render(request, 'set_session_login.html')
    else:
        #接收接口参数
        uname = request.POST.get('uname','')
        pwd = request.POST.get('pwd','')
        flag = request.POST.get('flag','')
        #判断是否登录成功
        if uname=='zhangsan' and pwd =='123':
            request.session['login'] = uname
            user = UserCenter(uname,pwd)
            request.session['login_'] = jsonpickle.dumps(user) #把对象序列化成普通字符串存入session
            return HttpResponseRedirect('/cookie_session/usercenter/')
        return HttpResponseRedirect('/cookie_session/set_session_login/')
class UserCenter:
    """用户中心对象"""
    def __init__(self,uname,pwd):
        self.uname = uname
        self.pwd =pwd
    def __getstate__(self):
        """在jsonpickle序列化对象过滤对象某个属性时会引用这个"""
        data =self.__dict__.copy()
        del data['pwd']
        return data
    # def __setstate__(self, state):
    #     """在jsonpickle反序列化对象时文件file会引用这个"""
    #     pass


from django.views import View
class Class_Views(View):
    def get(self,request,*args,**kwargs):
        return  render(request,'class_views.html')
    def post(self,request,*args,**kwargs):
        pass


"""把图片显示在页面"""
#方法一：http://127.0.0.1:8000/view/static_views/7.png
class StaticViews(View):
    def get(self,request,*args,**kwargs):
        #获取文件名(访问路径)
        file_path = request.path
        import re
        file_group = re.match(r'/view/static_views/(.*)',file_path)
        filename = file_group.group(1)
        filedir = os.path.join(os.getcwd(),'static\images',filename)
        if not os.path.exists(filedir):
            raise Http404()
        return FileResponse(open(filedir,'rb'), content_type='image/png')#mime类型、！=image就会显示下载（'*/*'）
#方法二：http://127.0.0.1:8000/static/7.png
"""
1、修改settings中配置
STATIC_URL = '/static/'#地址栏中8000后面的路径
STATICFILES_DIRS = [
        os.path.join(BASE_DIR,'static\images'),
        os.path.join(BASE_DIR,'static\js'),
        os.path.join(BASE_DIR,'static\css'),
]#文件存储位置
"""
#方法三:http://127.0.0.1:8000/view/show_pic/
class ShowPic(View):
    def get(self,request,*args,**kwargs):
        return  render(request,'class_views.html')


"""模板渲染原理"""
def templates_views1(request):
    t = Template('hello:{name}')#模板对象
    c = Context({'name':'zhangsan'})
    renderStr = t.render(c)
    return HttpResponse(renderStr)
def templates_views2(request):
    with open('templates/404.html','rb') as fr:#打开流读取文件就成了字符串
        content = fr.read()
    t = Template(content)
    c = Context({'name': 'zhangsan'})
    renderStr = t.render(c)
    return HttpResponse(renderStr)
def templates_views3(request):
    t =loader.get_template('404.html')
    renderStr = t.render({'name': 'zhangsan'})
    return HttpResponse(renderStr)
def templates_views4(request):
    return render(request,'404.html')


def templates_lable(request):
    """模板标签语法"""
    return render(request,'templates_lable.html',{'key':{'key1':'value1','key2':'value2'},
                    'date':datetime.datetime.today(),'numList':[1,2,3],'title':'hello','autoescape ':'<h1>hello</h1>'})



class TestFilters(View):
    """过滤器"""
    def get(self,request):
        import datetime
        d = datetime.datetime.today()
        return render(request,'filter.html',{'num':8,'str':'abs','datetime':d})

class CustomFilters(View):
    """自定义过滤器"""
    def get(self,request):
        content = "### 自定义过滤器"#在Markdown中###表示加粗
        str = 'abcdef'
        return render(request,'filter.html',{'content':content,'str':str})

class ContextProsessors(View):
    """自定义全局上下文"""
    def get(self,request):
        t = Template('hello:{{uname}}')#引用模板对象渲染
        from project_test01.my_context_prosessors import getData
        context = RequestContext(request,dict_=None,processors=(getData,))# 相比下面的用法是当有多个方法都是用到了getData的返回，这样可以解决硬编码
        # context = Context({'name': 'zhangsan'})
        render_str = t.render(context)
        return HttpResponse(render_str)

class InheritTemplate(View):
    """模板继承"""
    def get(self,request):
        return  render(request,'base_child.html')

@csrf_protect
def csrf_token(request):
    """局部生效csrf_token校验"""
    return HttpResponse('post局部csrf_token')
@csrf_exempt
def csrf_token(request):
    """局部免除csrf_token校验"""
    return HttpResponse('post局部csrf_token')

from .forms import *
class TestFormsClass(View):
    """表单类渲染HTML--模型类与表单类独立"""
    def get(self,request):
        #创建forms无参的空对象
        login_form = LoginFormsClass()
        return render(request, 'LoginFormsClass.html', {'login_form':login_form})
    def post(self,request):
        """利用forms的内置方法"""
        login_form = LoginFormsClass(request.POST)#返回标签对象
        # 校验数据是否合法
        if login_form.is_valid():
            login_data = login_form.cleaned_data #返回的是一个字典
            sname = login_data['sname']
            pwd = login_data['password']
            """利用django自带user表完成校验"""
            # user = authenticate(username=login_data['sname'],pwd=login_data['pwd'])#去数据库表中进行匹配
            # user = authenticate(**login_data)#拆包
            # #判断是否登录成功
            # if user:
            #     #将用户信息保存到session中
            #     login(request,user)
            #     return  HttpResponse('登录成功')
            """利用之前获取页面响应数据完成校验"""
            # sname = request.POST.get('sname', '')
            # pwd = request.POST.get('password', '')
            user = LoginFormsClassModel.objects.filter(sname=sname).filter(password=pwd)
            if user:
                # 将用户信息保存到session中
                request.session['user'] = pwd
                return HttpResponse('登录成功')
        return HttpResponse('登录失败')



class TestModelFormsClass(View):
    """表单类渲染HTML--模型类与表单类相关联"""
    def get(self, request):
        #创建两个表单类的对象
        stu = StudentForms()
        cls = ClassForms()
        return render(request,'TestModelFormsClass.html',{'stu_form':stu,'cls_form':cls})
    def post(self,request):
        #创建表单类对象
        stu = StudentForms(request.POST)
        cls = ClassForms(request.POST)
        #校验表单类对象是否合法
        if stu.is_valid()*cls.is_valid():
            flag = stu.checkpwd()#利用表单类校验密码是否一致
            if flag:
                cls_form = cls.save()
                stu_form = stu.save(commit=False)  # commit=False表示事务未提交
                stu_form.clazz = cls_form#将数据库字段密码赋值
                stu_form.pwd = flag#将数据库字段密码赋值
                stu_form.confirm_pwd = flag
                stu_form.save()
                return HttpResponse('注册成功')
        #注册失败渲染之前的页面
        return  render(request,'TestModelFormsClass.html',{'stu_form':stu,'cls_form':cls})


class JsTemplatesCheck(View):
    """利用js编写html校验表单功能"""
    def get(self,request):
        return render(request, 'js_templates_check.html')


class TestAjax(View):
    """AJAX实现部分数据更新"""
    def get(self,request):
        return render(request,'test_ajax.html')
def get_ajax_data(request):
    uname = request.GET.get('uname','')
    pwd = request.GET.get('pwd','')
    return JsonResponse({'flag':True})
def post_ajax_data(request):
    uname = request.POST.get('uname','')
    pwd = request.POST.get('pwd','')
    return JsonResponse({'flag':True})

class AjaxLoginCheck(View):
    """利用ajax做用户名唯一校验"""
    def get(self,request):
        return render(request,'ajax_login_check.html')
def only_user(request):
    """ajax做用户唯一校验"""
    uname = request.GET.get('uname','')
    #判断数据库是否存在
    if uname=='zhangsan':#flag=Stu.objects.filter(uname=uname)
        return JsonResponse({'flag': False})
    else:
        return JsonResponse({'flag': True})


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
    stu = Student.objects.all()
    return render(request, 'index.html', {'stu': stu})

#django自带views层缓存
from django.views.decorators.cache import cache_page
# @cache_page(60*30)
def cache_view(request):
    stu = Student.objects.all()
    return render(request,'index.html',{'stu':stu})

def cache_redis(request):
    # 使用redis缓存
    redis_cache = caches['redis']  # 配置中也要选择redis
    redis_cache.set('zhangsan', '123')
    value = redis_cache.get('zhangsan')
    return HttpResponse(value)

