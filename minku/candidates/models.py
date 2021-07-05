from django.db import models
from django.contrib.auth.models import User
from datetime import datetime

from django.utils import timezone

YEAR_CHOICES = []
for r in range(1970, (datetime.now().year - 10)):
    YEAR_CHOICES.append((r, r))

GENDER = ((u'男', u'男'), (u'女', u'女'))
MARRIAGE_STATUS = ((u'已婚', u'已婚'), (u'未婚', u'未婚'))
DEGREE_TYPE = ((u'本科', u'本科'), (u'硕士', u'硕士'), (u'博士', u'博士'), (u'大专', u'大专'))
WORK_INTENTION = ((u'在职看机会', u'在职看机会'), (u'不看机会', u'不看机会'), (u'离职', u'离职'))
DEGREE_VALUE_TYPE = ((u'985/211', u'985/211'), (u'统招本科', u'统招本科'))


class Candidate(models.Model):
    # 基本信息
    basic_username = models.CharField(max_length=32, verbose_name=u'姓名')
    basic_user_status = models.CharField(max_length=64, blank=True, verbose_name=u'目前状态')
    basic_gender = models.CharField(max_length=2, choices=GENDER, blank=True, verbose_name=u'性别')
    basic_born_year = models.IntegerField(choices=YEAR_CHOICES, default=1990, verbose_name=u'出生年份')
    basic_age = models.IntegerField(default=0, verbose_name=u'年龄')
    basic_residence_city = models.CharField(max_length=64, blank=True, verbose_name=u'户籍')
    basic_phone = models.CharField(max_length=32, blank=True, unique=True, null=True, verbose_name=u'手机号码')
    basic_email = models.EmailField(max_length=64, blank=True, unique=True, null=True, verbose_name=u'邮箱')
    basic_marriage_status = models.CharField(max_length=2, choices=MARRIAGE_STATUS, blank=True, verbose_name=u'婚姻状况')
    basic_work_start_year = models.IntegerField(choices=YEAR_CHOICES, default=2015, verbose_name=u'参加工作时间')
    basic_work_years = models.IntegerField(default=0, verbose_name=u'工作年限')
    # 学历信息
    basic_edu_degree = models.CharField(max_length=64, choices=DEGREE_TYPE, blank=True, verbose_name=u'学历')
    basic_is_unified = models.BooleanField(blank=False, verbose_name='统招')
    basic_is_985 = models.BooleanField(blank=False, verbose_name='985')
    basic_is_211 = models.BooleanField(blank=False, verbose_name='211')
    # 工作信息
    work_industry = models.CharField(max_length=64, blank=True, verbose_name=u'行业')
    work_city = models.CharField(max_length=64, blank=True, verbose_name=u'工作城市')
    work_company = models.CharField(max_length=64, blank=True, verbose_name=u'公司名称')
    work_position = models.CharField(max_length=64, blank=True, verbose_name=u'职位名称')
    work_salary = models.CharField(max_length=64, blank=True, verbose_name=u'年薪')
    work_salary_structure = models.CharField(max_length=512, blank=True, verbose_name=u'薪资结构')
    work_intention = models.CharField(max_length=16, choices=WORK_INTENTION, blank=True, verbose_name=u'工作意向')
    # 期望工作
    expect_industry = models.CharField(max_length=128, blank=True, verbose_name=u'期望行业')
    expect_city = models.CharField(max_length=128, blank=True, verbose_name=u'期望城市')
    expect_position = models.CharField(max_length=128, blank=True, verbose_name=u'期望职位')
    expect_salary = models.CharField(max_length=64, blank=True, verbose_name=u'期望年薪')
    # 自我评价
    self_judgement = models.TextField(max_length=2046, blank=True, verbose_name=u'自我评价')
    # 附加消息
    additional_comments = models.TextField(max_length=2046, blank=True, verbose_name=u'附加消息')

    # 录入者信息
    creator = models.CharField(max_length=32, blank=True, verbose_name=u'候选人数据的创建人')
    created_date = models.DateTimeField(auto_now_add=True, verbose_name=u'创建时间')
    modified_date = models.DateTimeField(auto_now=True, null=True, blank=True, verbose_name=u'更新时间')
    last_editor = models.CharField(max_length=32, blank=True, verbose_name=u'最后编辑者')

    def get_age(self):
        origin_age = int(self.basic_age)
        latest_age = int(datetime.today().year) - int(self.basic_born_year)
        if latest_age != origin_age:
            self.basic_age = int(datetime.today().year) - int(self.basic_born_year)
            self.save()
        return latest_age

    class Meta:
        db_table = u'candidate'
        verbose_name = u'简历库'
        verbose_name_plural = u'简历库'

    def __str__(self):
        return self.basic_username


class EduRecords(models.Model):
    # 学校与学历信息
    edu_school = models.CharField(max_length=128, blank=True, verbose_name=u'学校')
    edu_degree = models.CharField(max_length=128, choices=DEGREE_TYPE, blank=True, verbose_name=u'学历')
    edu_major = models.CharField(max_length=128, blank=True, verbose_name=u'专业')
    edu_start_date = models.CharField(max_length=128, blank=True, verbose_name=u'入学时间')
    edu_end_date = models.CharField(max_length=128, blank=True, verbose_name=u'毕业时间')
    edu_degree_value = models.CharField(max_length=32, choices=DEGREE_VALUE_TYPE, blank=True, verbose_name=u'学校性质')
    candidate = models.ForeignKey(to=Candidate, on_delete=models.CASCADE)

    # 录入者信息
    creator = models.CharField(max_length=32, blank=True, verbose_name=u'候选人数据的创建人')
    created_date = models.DateTimeField(auto_now_add=True, verbose_name=u'创建时间')
    modified_date = models.DateTimeField(auto_now=True, null=True, blank=True, verbose_name=u'更新时间')
    last_editor = models.CharField(max_length=32, blank=True, verbose_name=u'最后编辑者')

    class Meta:
        db_table = u'edu_records'
        verbose_name = u'教育经历'
        verbose_name_plural = u'教育经历'

    def __str__(self):
        return self.edu_school


class CompanyRecords(models.Model):
    # 工作经历
    work_company = models.CharField(max_length=128, blank=True, verbose_name=u'公司')
    work_company_type = models.CharField(max_length=128, blank=True, verbose_name=u'公司性质')
    work_start_date = models.CharField(max_length=128, blank=True, verbose_name=u'入职时间')
    work_end_date = models.CharField(max_length=128, blank=True, verbose_name=u'离职时间')
    work_position = models.CharField(max_length=128, blank=True, verbose_name=u'职位')
    work_department = models.CharField(max_length=128, blank=True, verbose_name=u'所在部门')
    work_subordinate = models.CharField(max_length=128, blank=True, verbose_name=u'下属人数')
    work_report_to = models.CharField(max_length=128, blank=True, verbose_name=u'汇报对象')
    work_achievements = models.TextField(max_length=2046, blank=True, verbose_name=u'职责业绩')
    candidate = models.ForeignKey(to=Candidate, on_delete=models.CASCADE)

    # 录入者信息
    creator = models.CharField(max_length=32, blank=True, verbose_name=u'候选人数据的创建人')
    created_date = models.DateTimeField(auto_now_add=True, verbose_name=u'创建时间')
    modified_date = models.DateTimeField(auto_now=True, null=True, blank=True, verbose_name=u'更新时间')
    last_editor = models.CharField(max_length=32, blank=True, verbose_name=u'最后编辑者')

    class Meta:
        db_table = u'company_records'
        verbose_name = u'工作经历'
        verbose_name_plural = u'工作经历'

    def __str__(self):
        return self.work_company


class ProjectRecords(models.Model):
    # 项目经验信息
    project = models.CharField(max_length=128, blank=True, verbose_name=u'项目名称')
    project_company = models.CharField(max_length=128, blank=True, verbose_name=u'所在公司')
    project_start_date = models.CharField(max_length=128, blank=True, verbose_name=u'开始时间')
    project_end_date = models.CharField(max_length=128, blank=True, verbose_name=u'结束时间')
    project_position = models.TextField(max_length=2046, blank=True, verbose_name=u'项目职务')
    project_description = models.TextField(max_length=2046, blank=True, verbose_name=u'项目描述')
    project_responsibility = models.TextField(max_length=2046, blank=True, verbose_name=u'项目职责')
    project_achievements = models.TextField(max_length=2046, blank=True, verbose_name=u'项目业绩')
    candidate = models.ForeignKey(to=Candidate, on_delete=models.CASCADE)

    # 录入者信息
    creator = models.CharField(max_length=32, blank=True, verbose_name=u'候选人数据的创建人')
    created_date = models.DateTimeField(auto_now_add=True, verbose_name=u'创建时间')
    modified_date = models.DateTimeField(auto_now=True, null=True, blank=True, verbose_name=u'更新时间')
    last_editor = models.CharField(max_length=32, blank=True, verbose_name=u'最后编辑者')

    class Meta:
        db_table = u'project_records'
        verbose_name = u'项目经验'
        verbose_name_plural = u'项目经验'

    def __str__(self):
        return self.project


class Comments(models.Model):
    # 评论
    comment_content = models.TextField(max_length=2046, blank=True, verbose_name=u'评论内容')
    candidate = models.ForeignKey(to=Candidate, on_delete=models.CASCADE)

    # 录入者信息
    creator = models.CharField(max_length=32, blank=True, verbose_name=u'候选人数据的创建人')
    created_date = models.DateTimeField(default=timezone.now, verbose_name=u'创建时间')
    modified_date = models.DateTimeField(auto_now=True, null=True, blank=True, verbose_name=u'更新时间')
    last_editor = models.CharField(max_length=32, blank=True, verbose_name=u'最后编辑者')

    class Meta:
        db_table = u'comments'
        verbose_name = u'评论'
        verbose_name_plural = u'评论'

    def __str__(self):
        return self.creator
