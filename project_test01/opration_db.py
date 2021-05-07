from project_test01.models import *
#封装通过操作对象来操作数据库打印出执行的sql eg:Film.objects.all()
from django.db import connection
def opration_db():
    return connection.queries[-1]['sql']
# 所有的继承models.Model的类都有一个objects对象（管理器）(可以在控制台中执行)
#一、单表查询操作
#1、查询单个对象--结果必须只有一个，没有或者多余都会报错（objects.get()）
Film.objects.get(id=1) #返回的是一个对象
Film.objects.filter(id=1) #返回的是一个query_set 对象列表
#获得第一个
Film.objects.first()
#获得最后一个
Film.objects.last()
#获得记录总数
Film.objects.count()
#2、查询多个对象
Film.objects.all() #获取表中所有的数据
list = Film.objects.all()[2:4] #利用切片来做分页
#3、模糊查询
Film.objects.filter(mname__startswith='中国')
Film.objects.filter(mname__contains='中国')
#4、完全相等
Film.objects.filter(mname__exact='中国')
Film.objects.filter(mname='中国')
#5、忽略大小写
Film.objects.filter(mname__istartswith='h')
#6、是否为null
Film.objects.filter(mname__isnull=True)
#7、多条件查询
Film.objects.filter(mname__contains='h',mdesc='123')
Film.objects.filter(mname__contains='h').filter(mdesc='123')
#8、查询相应的字段（部分查询）
Film.objects.values('mname','mdesc').filter(mname__contains='h')
#9、排除一部分
Film.objects.filter(mname__contains='h').exclude(id=1)
#10、排序
Film.objects.order_by(id) #升序、降序-->-id
#11、日期查询
Film.objects.filter(id__gt=1)#大于1
Film.objects.filter(id__lt=1)#小于1
Film.objects.filter(id__lte=1)#小于等于
Film.objects.filter(id__in=(1,3))#跟数据库in一样
Film.objects.filter(id__range=(1,3))#1,2,3--跟数据库的between--and--一样

#二、单表增删改
#1、增
#方法一
Film.objects.create(id=1,mname=1234,mdesc='haha')
#方法二
film = Film(id=1,mname=1234,mdesc='haha')
film.save()
#2、删除
#方法一
Film.objects.filter(id=1).delete()
#方法二
film = Film.objects.filter(id=1)
film.delete()
#3、修改
#方法一（更新所有字段，效率低 可以看下执行的sql）
film = Film.objects.filter(id=1)
film.mname = 'wangwu'
film.save()
#方法二(必须是用filter才能用update ，因为filter返回的是query_set)
Film.objects.filter(id=2).update(mname='mazi')

#三、创建单表--常用字段类型
'''
CharField max_length(输入框)
TextField (没有长度限制的文本域--字符串)
DateField (日期)
DateTimeField (日期+时间)
BooleanField (真假 Ture/Faulse)
NullBooleanField Null (真假 null)
Integer 
PositiveIntegerField (正整数)
DecimalField (浮点型 max_digits,decimal_places)
ImageField (图片依赖pillow包处理图片，upload_to='upload'指定文件上传到项目相对路径upload目录)
FileField (ImageField继承FileField，upload_to='upload')
EmailField （默认会校验是否是邮箱格式）
AutoField (自动递增--给主键)
ForeignKey (外键 1:n 一表对多表)
ManyToManyField (n:n 多表对多表)
UUIDField(唯一的) 获取uuid-->import uuid  uuid.uuid4().get_hex()-->字符串
auto_now_add=True 第一次插入数据时会更新这个字段，自动更新为当前时间
auto_now=True 自动更新为当前时间
default=True 默认值
unique 字段唯一
null=Ture (字段可以为空)
on_delete=models.CASCADE 级联删除
'''

#四、创建多表
#1、一对一 Student-->Card
'''
class Student(models.Model):
    stu_id = models.AutoField(primary_key=True)
    sname = models.CharField(max_length=32)
class Card(models.Model):
    card_id = models.OneToOneField(Student, primary_key=True,
                                   on_delete=models.CASCADE)  # related_name='sys_card' 不写name='sys_card' 那这个表默认是项目名+小写表名card
    major = models.CharField(max_length=16)
#插入多表数据
stu = Student(sname=u'zhangsan')
card = Card(card_id=stu,major=u'计算机')
stu.save()
card.save()
#多表查询
#正向查询
major = Student.objects.first().card #(等于Card.objects.first())
#逆向查询（通过OneToOneField表去查另一张表）
sname = Card.objects.first().card_id
'''

# 创建多表Student C_Class (一对多)
'''
class C_Class(models.Model):  # 主表
    c_no = models.AutoField(primary_key=True)
    cname = models.CharField(max_length=32)
class C_Student(models.Model):  # 从表
    stu_id = models.AutoField(primary_key=True)
    sname = models.CharField(max_length=32)
    c_no = models.ForeignKey(C_Class, on_delete=models.CASCADE,
                             related_name='student')  # related_name='student' 不写related_name='c_student' 那这个表默认是小写表名card
#插入数据
cls1 = C_Class.objects.create(cname=u'201python')
cls2 = C_Class.objects.create(cname=u'201java')
stu1 = C_Student.objects.create(sname=u'zhangsan',c_no=cls1)
stu2 = C_Student.objects.create(sname=u'zhangsan',c_no=cls2)
stu3 = C_Student.objects.create(sname=u'lisi',c_no=cls1)
def insert_Data(clsname, *sname):  # *表示可变参数
    try:
        cls = C_Class.objects.get(cname=clsname)  # get没有值会报错
    except C_Class.DoesNotExist:
        cls = C_Class.objects.create(cname=clsname)
    for s in sname:
        try:
            C_Student.objects.get(sname=s)  # get没有值会报错
        except C_Student.DoesNotExist:
            C_Student.objects.create(sname=s, c_no=cls)
insert_Data('202HTML5','wangwu','mazi')
#查询数据
var_list = C_Class.objects.first().student.all()   ( C_Class.objects.first().c_student_set.all())--查询出的是query_set
var = C_Student.objects.first().c_no
'''

# 创建多表Course Teacher (多对多)--会自动创建一张中间表
'''
class Course(models.Model):
    course_no = models.AutoField(primary_key=True)
    course_name = models.CharField(max_length=32)
class Teacher(models.Model):
    teacher_no = models.AutoField(primary_key=True)
    teacher_name = models.CharField(max_length=16)
    mid_cou_no = models.ManyToManyField(Course)
#插入数据
cour1 = Course.objects.create(course_name='python')
cour2 = Course.objects.create(course_name='java')
cour3 = Course.objects.create(course_name='C')
teac = Teacher.objects.create(teacher_name='zhangsan')
teac.mid_cou_no.add(cour1,cour2)
def insert_Data_ManyToMany(tname,*coursenames):
    try:
        teac = Teacher.objects.get(teacher_name=tname)
    except Teacher.DoesNotExist:
        teac = Teacher.objects.create(teacher_name=tname)
    courList = []
    for cour in coursenames:
        try:
            course = Course.objects.get(course_name=cour)
        except Course.DoesNotExist:
            course = Course.objects.create(course_name=cour)
        courList.append(course)
    teac.mid_cou_no.add(*courList)#解包
insert_Data_ManyToMany('laowang','mysql','oracle')
#查询
#正向查询
Course.objects.first().teacher_set.all()
#逆向查询
Teacher.objects.first().mid_cou_no.all()
*args-->入参元祖 1，2
**args-->入参字典1，2，c='1'
*用在形参中表示可变参数，在实参中表示解包

'''
#5、既有多对一又有多对多
class SCourse(models.Model):
    course_no = models.AutoField(primary_key=True)
    course_name = models.CharField(max_length=32)
    def __str__(self):
        return u'SCourse:%s'%self.course_name
    class Meta:
        db_table = 'S_course'
class SClass(models.Model):
    c_no = models.AutoField(primary_key=True)
    cname = models.CharField(max_length=32)
    def __str__(self):
        return u'S_Class:%s' % self.cname
    class Meta:
        db_table = 'S_class'
class SStudent(models.Model):
    sno = models.AutoField(primary_key=True)
    sname = models.CharField(max_length=32)
    s_cls = models.ForeignKey(SClass)  # related_name='student' 不写related_name='c_student' 那这个表默认是小写表名card
    s_cour = models.ManyToManyField(SCourse)
    def __str__(self):
        return u'SStudent:%s' % self.sname
    class Meta:
        db_table = 'S_student'
def registerStu(sname,cname,*cournames):
    """插入班级表"""
    #获取班级对象并插入数据
    cls = getCls(cname)
    #获取课程对象列表并插入数据
    courList = getCourList(*cournames)
    #插入学生表数据
    try:
        stu = SStudent.objects.get(sname=sname)
    except SStudent.DoesNotExist:
        stu = SStudent.objects.create(sname=sname,s_cls=cls)
    #插入中间表数据
    stu.s_cour.add(*courList)
    return True
def getCls(cname):
    """根据班级名称获取班级对象"""
    try:
        cls = SClass.objects.get(cname=cname)
    except SClass.DoesNotExist:
        cls = SClass.objects.create(cname=cname)
    return cls
def getCourList(*cournames):
    """根据课程名称获取课程对象"""
    courList = []
    for courname in cournames:
        try:
            cour = SCourse.objects.get(course_name=courname)
        except SCourse.DoesNotExist:
            cour = SCourse.objects.create(course_name=courname)
        courList.append(cour)
    return courList

#6、自定义管理器



'''
# 聚合函数-->可以用showsql查看sql
from django.db.models import Max, Min, Count, Avg, Sum
SStudent.objects.aggregate(score_max=Max('score'))
SStudent.objects.aggregate(score_min=Min('score'))
SStudent.objects.aggregate(score_count=Count('*'))
# 分组聚合函数
SStudent.objects.values('cls').annotate(Count=Count('score'))  # 以班级分组，求出每个班级的人数
# 子查询
SStudent.objects.values('cls').annotate(sum=Sum('score')).aggregate(max=Max('sum'))  # 查询出每个班级成绩最高的人
# 关联查询
SStudent.objects.values("cls__cname")  # -->SStudent.objects.values("cls__c_id")
'''