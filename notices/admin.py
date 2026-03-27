from django.contrib import admin
from .models import Notice

@admin.register(Notice)
class NoticeAdmin(admin.ModelAdmin):
    list_display = ('title', 'created_at', 'institution', 'is_active')
    list_filter = ('institution', 'created_at', 'is_active')
