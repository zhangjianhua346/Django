from django.db import models


# Create your models here.
# 数据库模型对象

# 单表--用户注册


class User(models.Model):
    id = models.IntegerField(primary_key=True, auto_created=True)
    name = models.CharField(max_length=32)
    sname = models.CharField(max_length=32)
    spwd = models.CharField(max_length=16)

    class Meta:#Meta元数据中指定所属的应用
        db_table = 'sys_user'


# 单表--电影
class Film(models.Model):
    id = models.IntegerField(primary_key=True, auto_created=True)
    mname = models.CharField(max_length=32, unique=True)
    mdesc = models.CharField(max_length=64)
    mimg = models.CharField(max_length=32)
    mlink = models.CharField(max_length=16)

    def __str__(self):  # 对象输出
        return u'Film:%s' % self.mname

    # def __unicode__(self):
    #     return u'Film:%s' % self.mname

    class Meta:
        db_table = 'sys_film'
        # ordering = 'id'#默认排序


# 创建多表Student Card (一对一)
class Student(models.Model):
    stu_id = models.AutoField(primary_key=True)
    sname = models.CharField(max_length=32)

    def __str__(self):
        return u'Student:%s' % self.sname

    class Meta:
        db_table = 'Student'


class Card(models.Model):
    card_id = models.OneToOneField(Student, primary_key=True,
                                   on_delete=models.CASCADE)  # related_name='sys_card' 不写name='sys_card' 那这个表默认是项目名+小写表名card
    major = models.CharField(max_length=16)

    def __str__(self):
        return u'Card:%s' % self.major
        # return u'Card:%s' %Student.sname

    class Meta:
        db_table = 'Card'


# #插入多表数据
# stu = Student(sname=u'zhangsan')
# card = Card(card_id=stu,major=u'计算机')
# stu.save()
# card.save()
# #多表查询
# #正向查询
# major = Student.objects.first().card #(等于Card.objects.first())
# #逆向查询（通过OneToOneField表去查另一张表）
# sname = Card.objects.first().card_id



# 创建多表Student C_Class (一对多)
class C_Class(models.Model):  # 主表
    c_no = models.AutoField(primary_key=True)
    cname = models.CharField(max_length=32)

    def __str__(self):
        return u'C_Class:%s' % self.cname

    class Meta:
        db_table = 'C_Class'


class C_Student(models.Model):  # 从表
    stu_id = models.AutoField(primary_key=True)
    sname = models.CharField(max_length=32)
    c_no = models.ForeignKey(C_Class, on_delete=models.CASCADE,
                             related_name='student')  # related_name='student' 不写related_name='c_student' 那这个表默认是小写表名card

    def __str__(self):
        return u'Student:%s' % self.sname

    class Meta:
        db_table = 'C_Student'


# #插入数据
# cls1 = C_Class.objects.create(cname=u'201python')
# cls2 = C_Class.objects.create(cname=u'201java')
# stu1 = C_Student.objects.create(sname=u'zhangsan',c_no=cls1)
# stu2 = C_Student.objects.create(sname=u'zhangsan',c_no=cls2)
# stu3 = C_Student.objects.create(sname=u'lisi',c_no=cls1)
def insert_Data_OneToMany(clsname, *sname):  # *表示可变参数
    try:
        cls = C_Class.objects.get(cname=clsname)  # get没有值会报错
    except C_Class.DoesNotExist:
        cls = C_Class.objects.create(cname=clsname)
    for s in sname:
        try:
            C_Student.objects.get(sname=s)  # get没有值会报错
        except C_Student.DoesNotExist:
            C_Student.objects.create(sname=s, c_no=cls)


# insert_Data_OneToMany('202HTML5','wangwu','mazi')
# #查询数据
# var_list = C_Class.objects.first().student.all()   ( C_Class.objects.first().c_student_set.all())--查询出的是query_set
# var = C_Student.objects.first().c_no



# 创建多表Course Teacher (多对多)--会自动创建一张中间表
class Course(models.Model):
    course_no = models.AutoField(primary_key=True)
    course_name = models.CharField(max_length=32)

    def __str__(self):
        return u'Course:%s' % self.course_name

    class Meta:
        db_table = 'sys_course'


class Teacher(models.Model):
    teacher_no = models.AutoField(primary_key=True)
    teacher_name = models.CharField(max_length=16)
    mid_cou_no = models.ManyToManyField(Course)

    def __str__(self):
        return u'Teacher:%s' % self.teacher_name

    class Meta:
        db_table = 'sys_teacher'


# 插入数据
# cour1 = Course.objects.create(course_name='python')
# cour2 = Course.objects.create(course_name='java')
# cour3 = Course.objects.create(course_name='C')
# teac = Teacher.objects.create(teacher_name='zhangsan')
# teac.mid_cou_no.add(cour1,cour2)
def insert_Data_ManyToMany(tname, *coursenames):
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
    teac.mid_cou_no.add(*courList)  # 解包


# insert_Data_ManyToMany('laowang','mysql','oracle')
# #查询
# #正向查询
# Course.objects.first().teacher_set.all()
# #逆向查询
# Teacher.objects.first().mid_cou_no.all()



from django.db.models.manager import Manager


# 高级实现自定义管理器--重写create
# 实现SStudent.objects.create(sname='lisi',s_cls='B203python',s_cour=('html5','java','python'))
class CustomManagerStudent(Manager):
    def create(self, **kwargs):
        # 先班级表入库操作
        cls = getCls(kwargs['s_cls'])  # kwargs.get('s_cls')
        kwargs['s_cls'] = cls  # 把s_cls的value替换成对象，因为后面学生表入库操作用到的是SClass对象
        # 课程表入库操作
        cour_list = kwargs.pop('s_cour')  # 因为学生表只要两个字段入参sname，s_cls -->create(sname=sname,s_cls=cls)
        courList = getCourList(*cour_list)
        # 学生表入库操作
        stu = Manager.create(self, **kwargs)  # 左边写的是调用原生的create，=SStudent.objects.create(sname=sname,s_cls=cls)
        # 学生课程的中间表入库操作
        stu.s_cour.add(*courList)


# 多表（既有多对一又有多对多）
class SCourse(models.Model):
    course_no = models.AutoField(primary_key=True)
    course_name = models.CharField(max_length=32)

    def __str__(self):
        return u'SCourse:%s' % self.course_name

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
    s_cls = models.ForeignKey(SClass, on_delete=models.CASCADE)  # related_name='student' 不写related_name='c_student' 那这个表默认是小写表名card
    s_cour = models.ManyToManyField(SCourse)  # 中间表字段

    def __str__(self):
        return u'SStudent:%s' % self.sname

    class Meta:
        db_table = 'S_student'

    objects = CustomManagerStudent()  # 重写管理器


def registerStu(sname, cname, *cournames):
    """插入班级表"""
    # 获取班级对象并插入数据
    cls = getCls(cname)
    # 获取课程对象列表并插入数据
    courList = getCourList(*cournames)
    # 插入学生表数据
    try:
        stu = SStudent.objects.get(sname=sname)
    except SStudent.DoesNotExist:
        stu = SStudent.objects.create(sname=sname, s_cls=cls)
    # 插入中间表数据
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


# 自定义管理器 Manager(重写方法)
from django.db.models.manager import Manager


class CustomManager(Manager):
    def all(self):
        return Manager.all(self).filter(
            is_delete=True)  # Manager = objects,self 指的是本身的,Manager.all(self)父类本身的 -->类似java的this
        # return Manager.get_queryset(self).filter(is_delete =True)


# class BatchManager(Manager):
#     def filter(self, *args, **kwargs):
#         # 1、获取要删除的记录
#         deleteList = Manager.get_queryset(self)
#
#         # 定义一个闭包方法执行修改is_delete=Ture操作
#         def delete1(deleteList):
#             for de in deleteList:
#                 de.is_delete = True
#                 de.save()
#
#         # return delete
#         import \
#             types  # Python2是new   new.instancemethod=types.MethodType,deleteList.delete = new.instancemethod(delete,deleteList,QuerySet)
#         deleteList.delete = types.MethodType(delete1, deleteList)  # 动态创建实例方法，对外调用deleteList.delete ，实际执行的是右边的方法
#         return deleteList
#
#     def get_queryset(self):
#         return Manager.get_queryset(self).filter(is_delete=False)


# class TStudent(models.Model):
#     id = models.AutoField(primary_key=True)
#     sname = models.CharField(max_length=31)
#     is_delete = models.BooleanField(default=False)
#
#     def __str__(self):
#         return 'TStudent:%s' % self.sname
#
#     class Meta:
#         db_table = 'T_student'
#
#     # objects = CustomManager()#模型类中引用自定义管理器
#     objects = BatchManager()
#
#     def update(self):  # 重写修改数据库的方法
#         """
#
#         :rtype: object
#         """
#         self.isdelete = True
#         self.save()


'''
# stus = TStudent.objects.all()  # 自定义后调用的就是咱们自定义后的方法
# 一个模型类可以定义多个管理器，默认是调用objects管理器
s = TStudent.objects.filter().delete()
'''


# 自定义管理器--重写save方法
# 要实现stu=RStudent(sname='zhangsan', score=88, cls=RClass(cname='B202python班')) stu.save()-->直接save会报错，因为还没有先入库操作class对象(两个表的插入有先后顺序)
class RClass(models.Model):
    c_id = models.AutoField(primary_key=True)
    cname = models.CharField(max_length=18)
class RStudent(models.Model):
    s_id = models.AutoField(primary_key=True)
    sname = models.CharField(max_length=8)
    score = models.PositiveIntegerField()
    cls = models.ForeignKey(RClass, default=False, on_delete=models.CASCADE)
    def save(self, force_insert=False, force_update=False, using=None, update_fields=None):  # 重写save方法
        try:
            clas = RClass.objects.get(cname=self.cls.cname)
        except RClass.DoesNotExist:
            clas = RClass.objects.create(cname=self.cls.cname)
        self.cls = clas
        models.Model.save(self, force_insert=False, force_update=False, using=None,
                          update_fields=None)  # 学生表的插入 =stu.save() -->stu就是RStudent的一个对象
# stu=RStudent(sname='zhangsan', score=88, cls=RClass(cname='B202python班'))
# stu.save()

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


'''
#原生查询数据库
#1、包含主键（raw，python3会报必须含有主键的错？？）
# stus = SStudent.objects.raw('select * from project_test01_rstudent') #-->返回的是query_set,用raw返回的参数中必须要包括主键
# for stu in stus:
#     print(stu)
#2、可以包或者不包含主键
from django.db import connection
with connection.cursor() as cursor:  # -->cursor = connection.cursor()#指针，游标
    cursor.execute('select sname,score from project_test01_rstudent')
    cur_list = cursor.fetchall()  # 查询所有 .fetchone()查询第一条
    for cur in cur_list:
        print(cur)
    #cursor.close() 用了with函数会自动关闭 -->cursor有__exit__函数
'''


#Q和F查询（条件查询）
from django.db.models import Q,F
# SStudent.objects.filter(Q(sname='zhangsan')&Q(score='88'))#查询名字为张三且分数为88
# SStudent.objects.filter(Q(sname='zhangsan')|Q(score='88'))#查询名字为张三或分数为88
# SStudent.objects.filter(~Q(sname='zhangsan'))#查询名字为非张三
# SStudent.objects.filter(s_id=1).update(score=F('score')+10)#update只能用于query_set对象,将学号为1的学生成绩修改+10分
# SStudent.objects.filter(s_id__gt=1).update(score=F('score')+10)#将学号大于等于1的学生成绩修改+10分--批量修改


"""
#事务（保证数据库数据的安全性）
事务的基本特性：
1、原子性：要么都做、要么全不做
2、一致性：事务开始前和结束后，数据库的完整性约束没有被破坏
3、隔离性：同一时间，只允许一个事务请求同一数据，不同事务间彼此没有任何干扰
4、持久性：事务完成后，被保存到数据库不能回滚

事务的并发问题：
1、脏读：事务A读取了事务B更新的数据，但是B回滚了操作，那么A读到的数据是脏数据
2、不可重复读：事务A多次读取同一数据，事务B在事务A多次读取过程中，对数据做了更新并提交，导致A事务多次读取同一数据时结果不一致（侧重修改）
3、幻读：要将表中的数据全部逻辑删除，在同一时刻有新的数据创建，最后发现还有一条数据没有逻辑删除（侧重新建/删除）
"""
from django.db.transaction import atomic
@atomic
def test_atomic():
    RStudent.objects.create(sname='zhangsan', score=88, cls=RClass(cname='B202python班'))


class File_Student(models.Model):
    """文件上传"""
    sno = models.AutoField(primary_key=True)
    sname = models.CharField(max_length=32)
    photo = models.ImageField(upload_to='imgs')#默认会加上MEDIA_ROOT路径默认为''
    def __str__(self):
        return u'File_Student:%s'%self.sname
    class Meta:
        db_table = 'File_Student'


class LoginFormsClassModel(models.Model):
    """定义一个表单类对应的模型类--模型类与表单类相独立"""
    sname = models.CharField(max_length=32)
    password = models.CharField(max_length=16)
    def __str__(self):
        return u'LoginFormsClass%s'%self.sname
    class Meta:
        db_table = 'LoginFormsClass'

class ModelClassForms(models.Model):
    """定义一个表单类对应的模型类--模型类与表单类相关联"""
    cno = models.AutoField(primary_key=True)
    cname = models.CharField(max_length=32,verbose_name=u'班级')
    def __str__(self):
        return u'ModelClassForms:%s'%self.cname
    class Meta:
        db_table = 'ModelClassForms'
class ModelStudentForms(models.Model):
    """定义一个表单类对应的模型类--模型类与表单类相关联"""
    sno = models.AutoField(primary_key=True)
    sname = models.CharField(max_length=32,verbose_name=u'姓名')
    pwd = models.CharField(max_length=16,verbose_name=u'原密码')
    confirm_pwd = models.CharField(max_length=16,verbose_name=u'确认密码')
    clazz = models.ForeignKey(ModelClassForms,on_delete=models.CASCADE)
    def __str__(self):
        return u'ModelStudentForms:%s'%self.sname
    class Meta:
        db_table = 'ModelStudentForms'





from django.db import models
from pygments.lexers import get_all_lexers         # 一个实现代码高亮的模块
from pygments.styles import get_all_styles
LEXERS = [item for item in get_all_lexers() if item[1]]
LANGUAGE_CHOICES = sorted([(item[1][0], item[0]) for item in LEXERS]) # 得到所有编程语言的选项
STYLE_CHOICES = sorted((item, item) for item in get_all_styles())     # 列出所有配色风格
class RestFulAPI(models.Model):
    """实现api"""
    created = models.DateTimeField(auto_now_add=True)
    title = models.CharField(max_length=100, blank=True, default='')
    code = models.TextField()
    linenos = models.BooleanField(default=False)
    language = models.CharField(choices=LANGUAGE_CHOICES, default='python', max_length=100)
    style = models.CharField(choices=STYLE_CHOICES, default='friendly', max_length=100)

    class Meta:
        ordering = ('created',)

