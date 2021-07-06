from django.db import models
from django.contrib.auth.models import User
from datetime import datetime
from django.utils import timezone


class ColdCall(models.Model):
    # 基本信息
    basic_username = models.CharField(max_length=64, verbose_name=u'姓名')
    basic_gender = models.CharField(max_length=64, blank=True, verbose_name=u'性别')
    basic_region = models.CharField(max_length=64, blank=True, verbose_name=u'城市区域')
    basic_phone = models.CharField(max_length=64, blank=True, verbose_name=u'电话')
    basic_email = models.EmailField(max_length=64, blank=True, verbose_name=u'邮箱')
    basic_edu_school = models.CharField(max_length=64, blank=True, verbose_name=u'毕业院校')
    work_company = models.CharField(max_length=64, blank=True, verbose_name=u'公司')
    work_depart = models.CharField(max_length=64, blank=True, verbose_name=u'部门')
    work_position = models.CharField(max_length=64, blank=True, verbose_name=u'职位')
    additional_comments = models.TextField(max_length=2046, blank=True, verbose_name=u'备注')

    # 录入者信息
    cc_creator = models.CharField(max_length=32, blank=True, verbose_name=u'创建人')
    cc_created_date = models.DateTimeField(auto_now_add=True, verbose_name=u'创建时间')
    cc_modified_date = models.DateTimeField(auto_now=True, null=True, blank=True, verbose_name=u'更新时间')
    cc_last_editor = models.CharField(max_length=32, blank=True, verbose_name=u'最后编辑者')

    class Meta:
        db_table = u'cold_call'
        verbose_name = u'Cold Call'
        verbose_name_plural = u'Cold Call'
        unique_together = ('basic_username', 'basic_phone', 'work_company')

    def __str__(self):
        return self.basic_username


class Comments(models.Model):
    # 评论
    comment_content = models.TextField(max_length=2046, blank=True, verbose_name=u'评论')
    cold_call = models.ForeignKey(to=ColdCall, on_delete=models.CASCADE)

    # 录入者信息
    cc_comment_creator = models.CharField(max_length=32, blank=True, verbose_name=u'创建人')
    cc_comment_created_date = models.DateTimeField(default=timezone.now, verbose_name=u'创建时间')
    cc_comment_modified_date = models.DateTimeField(auto_now=True, null=True, blank=True, verbose_name=u'评论时间')
    cc_comment_last_editor = models.CharField(max_length=32, blank=True, verbose_name=u'最后编辑者')

    class Meta:
        db_table = u'cold_call_comments'
        verbose_name = u'评论'
        verbose_name_plural = u'评论'

    def __str__(self):
        return self.cc_comment_creator
