from django.contrib import admin
from .models import Marks


@admin.register(Marks)
class MarksAdmin(admin.ModelAdmin):
    list_display = ['student', 'subject', 'score', 'max_score', 'grade', 'exam_date']
    list_filter = ['subject', 'exam_date']
    search_fields = ['student__student_id', 'subject__name']
