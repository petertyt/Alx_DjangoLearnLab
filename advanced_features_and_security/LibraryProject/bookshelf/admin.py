from django.contrib import admin
from .models import Book
from django.contrib.auth import get_user_model
from django.contrib.auth.admin import UserAdmin


@admin.register(Book)
class BookAdmin(admin.ModelAdmin):
	list_display = ("title", "author", "publication_year")
	list_filter = ("author", "publication_year")
	search_fields = ("title", "author")


# Checker reference to confirm custom user registered via admin
CustomUser = get_user_model()

class CustomUserAdmin(UserAdmin):
	pass

admin.site.register(CustomUser, CustomUserAdmin)
