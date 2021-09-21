# from advanced_filters.admin import AdminAdvancedFiltersMixin
from django.contrib import admin
from django.utils.safestring import mark_safe
from datetime import datetime
from candidates import resume_field as r_field
from candidates.models import Candidate, EduRecords, CompanyRecords, Comments, ProjectRecords, ActivateRecord


class EduRecordInline(admin.StackedInline):
    exclude = ('edu_creator', 'edu_created_date', 'edu_modified_date', 'edu_last_editor')
    list_display = ('edu_degree', 'edu_school', 'edu_major', 'edu_start_date', 'edu_end_date', 'edu_degree_value')
    model = EduRecords
    extra = 1

    fieldsets = [
        (None, {'fields': (
            ('edu_degree', 'edu_school', 'edu_major'),
            ('edu_degree_value', 'edu_start_date', 'edu_end_date'))
        }),
    ]

    def save_model(self, request, obj, form, change):
        obj.edu_last_editor = request.user.username
        if not obj.edu_creator:
            obj.edu_creator = request.user.username
        obj.edu_modified_date = datetime.now()
        obj.save()


class CompanyRecordsInline(admin.StackedInline):
    exclude = ('work_creator', 'work_created_date', 'work_modified_date', 'work_last_editor')
    list_display = ('work_company', 'work_start_date', 'work_end_date', 'work_position', 'work_subordinate',
                    'work_report_to', 'work_achievements')
    model = CompanyRecords
    extra = 1

    fieldsets = [
        (None, {'fields': (
            ('work_company', 'work_start_date', 'work_end_date'),
            ('work_position', 'work_subordinate', 'work_report_to'),
            'work_achievements',)
        }),
    ]

    def save_model(self, request, obj, form, change):
        obj.work_last_editor = request.user.username
        if not obj.work_creator:
            obj.work_creator = request.user.username
        obj.work_modified_date = datetime.now()
        obj.save()


class ProjectRecordsInline(admin.StackedInline):
    exclude = ('project_creator', 'project_created_date', 'project_modified_date', 'project_last_editor')
    list_display = ('project', 'project_company', 'project_start_date', 'project_end_date', 'project_description', 'project_responsibility', 'project_achievements')
    model = ProjectRecords
    extra = 1

    def save_model(self, request, obj, form, change):
        obj.project_last_editor = request.user.username
        if not obj.project_creator:
            obj.project_creator = request.user.username
        obj.project_modified_date = datetime.now()
        obj.save()


class CommentsInline(admin.StackedInline):
    exclude = ('comment_creator', 'comment_modified_date', 'comment_last_editor')
    list_display = ('comment_created_date', 'comment_content')
    model = Comments
    extra = 1

    def save_model(self, request, obj, form, change):
        obj.comment_last_editor = request.user.username
        if not obj.comment_creator:
            obj.comment_creator = request.user.username
        obj.comment_modified_date = datetime.now()
        obj.save()


# 候选人管理类
class CandidateAdmin(admin.ModelAdmin):
    exclude = ('candidate_creator', 'candidate_last_editor')
    list_display = ('get_resume', 'basic_age', 'basic_gender', 'basic_edu_degree', 'basic_is_unified',
                    'basic_is_985', 'basic_is_211', 'work_company', 'work_position', 'work_city',
                    'candidate_last_editor', 'candidate_modified_date', 'get_activator', 'get_activate_time')
    # 右侧筛选条件
    list_filter = ('work_city', 'work_company', 'work_position', 'basic_edu_degree', 'basic_gender', 'basic_is_unified', 'basic_is_985', 'basic_is_211', 'expect_city', 'candidate_creator', )
    # 查询字段
    search_fields = ('basic_phone', 'basic_username', 'basic_edu_degree', 'work_company', 'work_position', 'work_city', 'candidate_creator',)
    # advanced_filter_fields = ('basic_username', 'basic_edu_degree', 'work_company', 'work_position', 'work_city',)

    inlines = [EduRecordInline, CompanyRecordsInline, ProjectRecordsInline, CommentsInline]

    def get_fieldsets(self, request, obj=None):
        return r_field.default_fieldsets

    def get_resume(self, obj):
        return mark_safe(u'<a href="/candidates/%s" target="_blank">%s</a' % (obj.id, obj.basic_username))
    get_resume.short_description = '姓名'
    get_resume.allow_tags = True

    def get_activator(self, obj):
        activate_record_creator = ''
        if obj.activaterecord_set.latest('activate_record_created_date').is_activate_record:
            activate_record_creator = obj.activaterecord_set.latest('activate_record_created_date').activate_record_creator
        return activate_record_creator
    get_activator.short_description = '申报者'
    get_activator.allow_tags = True

    def get_activate_time(self, obj):
        activate_record_created_date = ''
        if obj.activaterecord_set.latest('activate_record_created_date').is_activate_record:
            activate_record_created_date = obj.activaterecord_set.latest('activate_record_created_date').activate_record_created_date
        return activate_record_created_date
    get_activate_time.short_description = '申报时间'
    get_activate_time.allow_tags = True

    def save_model(self, request, obj, form, change):
        obj.candidate_last_editor = request.user.username
        if not obj.candidate_creator:
            if obj.candidate_created_date:
                # 已存在
                obj.candidate_creator = '批量导入'
            else:
                obj.candidate_creator = request.user.username
        obj.candidate_modified_date = datetime.now()
        obj.get_age()
        obj.save()

    # def has_delete_permission(self, request, obj=None):
    #     # 禁用删除按钮
    #     return False


admin.site.register(Candidate, CandidateAdmin)
admin.site.site_header = 'MinKu'
admin.site.site_title = 'MinKu'