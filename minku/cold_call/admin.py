from django.contrib import admin
from cold_call.models import ColdCall, Comments
from datetime import datetime


class CommentsInline(admin.StackedInline):
    exclude = ('cc_comment_creator', 'cc_comment_modified_date', 'cc_comment_last_editor')
    list_display = ('comment_content', 'comment_created_date')
    model = Comments
    extra = 1

    def save_model(self, request, obj, form, change):
        obj.cc_comment_last_editor = request.user.username
        if not obj.cc_comment_creator:
            obj.cc_comment_creator = request.user.username
        obj.cc_comment_modified_date = datetime.now()
        obj.save()


# 候选人管理类
class ColdCallAdmin(admin.ModelAdmin):
    exclude = ('cc_creator', 'cc_created_date', 'cc_modified_date', 'cc_last_editor')
    list_display = ('basic_username', 'work_company', 'work_depart', 'work_position', 'basic_region', 'basic_phone',
                    'additional_comments', 'basic_email', 'basic_edu_school', 'basic_gender')
    # 右侧筛选条件
    list_filter = ('work_company', 'work_depart', 'work_position', 'basic_region', 'basic_gender',)
    # 查询字段
    search_fields = ('work_company', 'work_depart', 'work_position', 'basic_region', 'additional_comments',)
    # advanced_filter_fields = ('basic_username', 'basic_edu_degree', 'work_company', 'work_position', 'work_city',)

    inlines = [CommentsInline]

    fieldsets = (
        ("基本信息", {'fields': (
            ("basic_username", "basic_gender", "basic_region", "basic_edu_school", "basic_phone", "basic_email"),
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
        obj.cc_last_editor = request.user.username
        if not obj.cc_creator:
            obj.cc_creator = request.user.username
        obj.cc_modified_date = datetime.now()

        obj.save()

# Register your models here.
admin.site.register(ColdCall, ColdCallAdmin)
admin.site.site_header = 'MinKu'
admin.site.site_title = 'MinKu'
