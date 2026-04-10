from django.contrib import admin
from .models import Fee


@admin.register(Fee)
class FeeAdmin(admin.ModelAdmin):
    list_display = ['student', 'description', 'amount', 'paid_amount', 'status', 'due_date']
    list_filter = ['status', 'due_date']
    search_fields = ['student__student_id']
