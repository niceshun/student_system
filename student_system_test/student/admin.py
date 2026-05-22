from django.contrib import admin
from student.models import Student
from django.conf import settings
from django.contrib.auth.models import User
from django.contrib.auth.hashers import make_password

class StudentAdmin(admin.ModelAdmin):
    # 配置展示列表，在User板块下的列表展示
    list_display = ('student_num', 'name', 'class_name', 'teacher_name', 'gender', 'birthday')
    # 配置过滤查询字段，在User板块下右侧过滤框
    list_filter = ('name', 'student_num')
    # 配置可以搜索的字段，在Teacher板块下右侧搜索框
    search_fields = (['name', 'student_num'])
    readonly_fields = ('teacher',)  # 设置只读字段，不允许更改
    # 定义列表显示的顺序，负号表示降序
    ordering = ('-created_at',)
    # 显示字段
    fieldsets = (
        (None, {
          'fields': ('student_num', 'name', 'gender', 'phone', 'birthday')
        }),
    )

    def save_model(self, request, obj, form, change):
        """
        添加student表时，同时添加到User表
        由于需要和teacher表级联，所以自动获取当前登录的老师id作为teacher_id
        """
        if not change:
            user = User.objects.create(
                username = request.POST.get('student_num'),  # 防止重名，用email作为用户名登录
                password = make_password(settings.STUDENT_INIT_PASSWORD),  # 密码加密
            )
            obj.user_id = user.id
            obj.teacher_id = request.user.id
        super().save_model(request, obj, form, change)
        return

    def delete_queryset(self, request, queryset):
        """
        删除多条记录
        同时删除user表中数据
        由于使用的是批量删除，所以需要遍历delete_queryset中的queryset
        """
        for obj in queryset:
            obj.user.delete()
        super().delete_model(request, queryset)
        return

    def delete_model(self, request, obj):
        """
        删除单条记录
        同时删除user表中的数据
        """
        super().delete_model(request, obj)
        if obj.user:
            obj.user.delete()
        return

# 绑定Student模型到StudentAdmin管理后台
admin.site.register(Student, StudentAdmin)





















































