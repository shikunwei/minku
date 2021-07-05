from django.contrib import admin
from cold_call.models import ColdCall, Comments
from datetime import datetime


class CommentsInline(admin.StackedInline):
    exclude = ('creator', 'created_date', 'modified_date', 'last_editor')
    list_display = ('comment_created_date', 'comment_content')
    model = Comments
    extra = 1

    def save_model(self, request, obj, form, change):
        obj.last_editor = request.user.username
        if not obj.creator:
            obj.creator = request.user.username
        obj.modified_date = datetime.now()
        obj.save()


# 候选人管理类
class ColdCallAdmin(admin.ModelAdmin):
    exclude = ('creator', 'created_date', 'modified_date', 'last_editor')
    list_display = ('basic_username', 'basic_gender', 'work_company', 'work_depart', 'work_position',
                    'basic_edu_school', 'basic_region', 'basic_phone',
                    'basic_phone2', 'basic_email', 'additional_comments')
    # 右侧筛选条件
    list_filter = ('work_company', 'work_depart', 'work_position', 'basic_region', 'basic_gender',)
    # 查询字段
    search_fields = ('work_company', 'work_depart', 'work_position', 'basic_region', 'additional_comments',)
    # advanced_filter_fields = ('basic_username', 'basic_edu_degree', 'work_company', 'work_position', 'work_city',)

    inlines = [CommentsInline]

    fieldsets = (
        ("基本信息", {'fields': (
            ("basic_username", "basic_gender", "basic_region", "basic_edu_school"),
            ("basic_phone", "basic_phone2", "basic_email"),
            ("work_company", "work_depart", "work_position"),
            ("additional_comments",))}),
    )
    #
    # def get_resume(self, obj):
    #     return mark_safe(u'<a href="/resumes/%s" target="_blank">%s</a' % (obj.id, "查看简历"))
    #
    # get_resume.short_description = '查看简历'
    # get_resume.allow_tags = True

    def save_model(self, request, obj, form, change):
        obj.last_editor = request.user.username
        if not obj.creator:
            obj.creator = request.user.username
        obj.modified_date = datetime.now()

        obj.save()

    # def has_delete_permission(self, request, obj=None):
    #     # 禁用删除按钮
    #     return False


# Register your models here.
admin.site.register(ColdCall, ColdCallAdmin)
admin.site.site_header = 'MinKu'
admin.site.site_title = 'MinKu'
