from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import User


@admin.register(User)
class CustomUserAdmin(UserAdmin):
    """
    Custom admin configuration for the User model.
    """
    list_display = ('username', 'email', 'first_name', 'last_name', 'is_staff', 'followers_count', 'following_count')
    list_filter = ('is_staff', 'is_superuser', 'is_active', 'created_at')
    search_fields = ('username', 'first_name', 'last_name', 'email')
    ordering = ('username',)
    
    fieldsets = UserAdmin.fieldsets + (
        ('Additional Info', {'fields': ('bio', 'profile_picture', 'followers')}),
    )
    
    add_fieldsets = UserAdmin.add_fieldsets + (
        ('Additional Info', {'fields': ('bio', 'profile_picture')}),
    )

