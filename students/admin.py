from django.contrib import admin
from .models import Department, Student, Subject


@admin.register(Department)
class DepartmentAdmin(admin.ModelAdmin):
    list_display = ['name']
    search_fields = ['name']


@admin.register(Subject)
class SubjectAdmin(admin.ModelAdmin):
    list_display = ['name', 'code', 'department']
    list_filter = ['department']


@admin.register(Student)
class StudentAdmin(admin.ModelAdmin):
    list_display = ['student_id', 'get_name', 'department', 'enrolled_date']
    list_filter = ['department']
    search_fields = ['student_id', 'user__first_name', 'user__last_name']

    def get_name(self, obj):
        return obj.user.get_full_name()
    get_name.short_description = 'Name'
