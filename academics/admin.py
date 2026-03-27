from django.contrib import admin
from .models import Class, Subject

@admin.register(Class)
class ClassAdmin(admin.ModelAdmin):
    list_display = ('name', 'section', 'institution', 'created_at')
    list_filter = ('institution',)

@admin.register(Subject)
class SubjectAdmin(admin.ModelAdmin):
    list_display = ('name', 'code', 'class_ref', 'teacher', 'institution', 'credits')
    list_filter = ('institution',)
