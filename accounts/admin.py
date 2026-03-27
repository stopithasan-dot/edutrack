from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import User

class CustomUserAdmin(UserAdmin):
    list_display = ('username', 'email', 'first_name', 'last_name', 'role', 'institution')
    fieldsets = UserAdmin.fieldsets + (
        ('EduTrack Information', {'fields': ('role', 'institution', 'phone', 'profile_picture', 'class_ref')}),
    )
    list_filter = UserAdmin.list_filter + ('role', 'institution')

admin.site.register(User, CustomUserAdmin)
