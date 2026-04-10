from django.contrib import admin
from .models import Session, Attendance


@admin.register(Session)
class SessionAdmin(admin.ModelAdmin):
    list_display = ['subject', 'date', 'start_time', 'is_active', 'qr_valid_until']
    list_filter = ['subject', 'date', 'is_active']


@admin.register(Attendance)
class AttendanceAdmin(admin.ModelAdmin):
    list_display = ['student', 'session', 'status', 'method', 'marked_at']
    list_filter = ['status', 'method', 'session__subject']
    search_fields = ['student__student_id']
