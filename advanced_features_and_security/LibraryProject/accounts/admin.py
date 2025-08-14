from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.contrib.admin.sites import AlreadyRegistered
from .models import CustomUser


class CustomUserAdmin(UserAdmin):
	fieldsets = (
		(None, {'fields': ('username', 'password')}),
		('Personal info', {'fields': ('first_name', 'last_name', 'email', 'date_of_birth', 'profile_photo')}),
		('Permissions', {'fields': ('is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions')}),
		('Important dates', {'fields': ('last_login', 'date_joined')}),
	)

	add_fieldsets = (
		(None, {
			'class': ('wide',),
			'fields': ('username', 'password1', 'password2', 'date_of_birth')
		}),
	)

	list_display = ('username', 'email', 'first_name', 'last_name', 'is_staff')
	search_fields = ('username', 'first_name', 'last_name', 'email')
	ordering = ('username',)


try:
	admin.site.register(CustomUser, CustomUserAdmin)
except AlreadyRegistered:
	pass
