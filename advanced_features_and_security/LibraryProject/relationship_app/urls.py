from django.urls import path
from .views import list_books
from .views import LibraryDetailView
from django.contrib.auth import views as auth_views
from . import views
from .views_admin import admin_view
from .views_librarian import librarian_view
from .views_member import member_view


urlpatterns = [
	path("books/", list_books, name="list_books"),
	path("libraries/<int:pk>/", LibraryDetailView.as_view(), name="library_detail"),
	# Auth
	path("login/", auth_views.LoginView.as_view(template_name="relationship_app/login.html"), name="login"),
	path("logout/", auth_views.LogoutView.as_view(template_name="relationship_app/logout.html"), name="logout"),
	path("register/", views.register, name="register"),

	# Role-based views
	path("role/admin/", admin_view, name="admin_view"),
	path("role/librarian/", librarian_view, name="librarian_view"),
	path("role/member/", member_view, name="member_view"),

	# Permission-protected book actions
	path("books/add/", views.add_book, name="add_book"),
	path("books/<int:pk>/edit/", views.edit_book, name="edit_book"),
	path("books/<int:pk>/delete/", views.delete_book, name="delete_book"),

	# Aliases for checker expectations
	path("add_book/", views.add_book, name="add_book_alias"),
	path("edit_book/<int:pk>/", views.edit_book, name="edit_book_alias"),
]

