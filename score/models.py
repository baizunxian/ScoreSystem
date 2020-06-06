from django.db import models

# Create your models here.


class Base(models.Model):
    create_time = models.DateTimeField('创建时间', auto_now_add=True)
    update_time = models.DateTimeField('更新时间', auto_now=True)

    class Meta:
        abstract = True
        verbose_name = "公共字段表"
        db_table = 'Base'


class AdminUser(Base):
    class Meta:
        verbose_name = "管理员"
        db_table = 'AdminUser'
    admin_name = models.CharField(verbose_name='用户名', max_length=255)
    admin_pwd = models.CharField(verbose_name='密码', max_length=255)



class Teacher(Base):
    class Meta:
        verbose_name = "老师表"
        db_table = 'Teacher'

    TName = models.CharField(verbose_name='用户名称', max_length=255, null=True)
    TStaff_number = models.IntegerField(verbose_name='职工号')
    TCollege = models.ForeignKey('College', models.CASCADE, verbose_name='老师学院', null=True)
    TMajor = models.IntegerField(verbose_name='老师专业', null=True)
    TPwd = models.CharField(verbose_name='密码', max_length=255)
    TSex = models.CharField(verbose_name='用户性别', max_length=255)
    TPhoneNumber = models.CharField(verbose_name='手机号码', max_length=255)
    TIDCard = models.CharField(verbose_name='身份证号', max_length=255)

    @classmethod
    def get_teacher_by_id(cls, TStaff_number=None):
        q = dict()
        if TStaff_number:
            q['TStaff_number'] = TStaff_number
        return cls.objects.filter(**q)


class Student(Base):
    class Meta:
        verbose_name = "学生表"
        db_table = 'Student'

    SName = models.CharField(verbose_name='用户名称', max_length=255, null=True)
    Student_id = models.IntegerField(verbose_name='学号')
    SCollege = models.ForeignKey('College', models.CASCADE, verbose_name='学院', null=True)
    SMajor = models.ForeignKey('Major', models.CASCADE, verbose_name='专业', null=True)
    SPwd = models.CharField(verbose_name='密码', max_length=255)
    SSex = models.CharField(verbose_name='用户性别', max_length=255)
    SPhoneNumber = models.CharField(verbose_name='手机号码', max_length=255)
    SIDCard = models.CharField(verbose_name='身份证号', max_length=255)

    @classmethod
    def get_student_by_id(cls, Student_id=None):
        q = dict()
        if Student_id:
            q['Student_id'] = Student_id
        return cls.objects.filter(**q)


class Bonus(Base):
    class Meta:
        verbose_name = "奖学金设置表"
        db_table = 'Bonus'

    bonus_name = models.CharField(verbose_name='奖项名称', max_length=255)
    credit_and_GPA = models.FloatField(verbose_name='学分和绩点', max_length=255)
    dormitory_standard = models.CharField(verbose_name='宿舍不达标次数', max_length=255)
    volunteer_hours = models.FloatField(verbose_name='志愿者小时数', max_length=255)
    credit = models.FloatField(verbose_name='学分', max_length=255)
    start_time = models.DateTimeField(verbose_name='开始时间', max_length=255)
    end_time = models.DateTimeField(verbose_name='结束时间', max_length=255)
    bonus_state = models.IntegerField(verbose_name='状态', default=0)
    bonus_type = models.CharField(verbose_name='奖金类型', max_length=255)
    Tuser = models.ForeignKey('Teacher', models.CASCADE, verbose_name='发布人')

    @classmethod
    def get_bonus_by_name(cls, bonus_name=None):
        q = dict()
        if bonus_name:
            q['bonus_name__icontains'] = bonus_name
        return cls.objects.filter(**q)


class Application(Base):
    class Meta:
        verbose_name = '申请表'
        db_table = 'Application'

    school_year = models.CharField(verbose_name='学年', max_length=255)
    college = models.ForeignKey('College', models.CASCADE, verbose_name='学院')
    major = models.ForeignKey('Major', models.CASCADE, verbose_name='专业')
    year_shift = models.CharField(verbose_name='年班', max_length=255)
    credit_and_GPA = models.FloatField(verbose_name='学分和绩点', max_length=255)
    dormitory_standard = models.CharField(verbose_name='宿舍不达标次数', max_length=255)
    volunteer_hours = models.FloatField(verbose_name='志愿者小时数', max_length=255)
    comprehensive_results = models.FloatField(verbose_name='综合成绩', max_length=255)
    activity_quantification = models.FloatField(verbose_name='活动量化', max_length=255)
    research_project = models.TextField(verbose_name='科研项目', max_length=255)
    remarks = models.TextField(verbose_name='申请理由', max_length=255)
    approval_remarks = models.TextField(verbose_name='审核备注', max_length=255, null=True)
    country_image = models.ImageField(verbose_name='国家奖', upload_to='country_image', blank=True, null=True)
    province_image = models.ImageField(verbose_name='省奖', upload_to='province_image', blank=True, null=True)
    school_image = models.ImageField(verbose_name='校奖', upload_to='school_image', blank=True, null=True)
    country_fraction = models.IntegerField(verbose_name='国家奖赋值分数', null=True)
    province_fraction = models.IntegerField(verbose_name='省奖赋值分数', null=True)
    school_fraction = models.IntegerField(verbose_name='校奖赋值分数', null=True)
    application_state = models.IntegerField(verbose_name='申请状态', default=0)
    Tuser = models.ForeignKey('Teacher', models.CASCADE, verbose_name='审核人', null=True)
    Suser = models.ForeignKey('Student', models.CASCADE, verbose_name='申请人')
    bonus = models.ForeignKey('Bonus', models.CASCADE, verbose_name='申请项目')

    @classmethod
    def get_search(cls, bonus_name=None, SName=None, college=None, major=None):
        q = dict()
        if bonus_name:
            q['bonus__bonus_name__icontains'] = bonus_name
        if SName:
            q['Suser__SName__contains'] = SName
        if college:
            q['college_id'] = college
        if major:
            q['major_id'] = major
        return cls.objects.filter(**q)


class College(Base):
    class Meta:
        verbose_name = '学院表'
        db_table = 'College'

    college_name = models.CharField(verbose_name='学院名', max_length=255)


class Major(Base):
    class Meta:
        verbose_name = '专业表'
        db_table = 'Major'

    college = models.ForeignKey('College', models.CASCADE, verbose_name='学院id')
    major_name = models.CharField(verbose_name='专业名', max_length=255)
