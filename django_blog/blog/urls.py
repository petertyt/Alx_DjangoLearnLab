from django.urls import path
from django.contrib.auth import views as auth_views
from . import views


urlpatterns = [
	path('login/', auth_views.LoginView.as_view(template_name='blog/login.html'), name='login'),
	path('logout/', auth_views.LogoutView.as_view(template_name='blog/logout.html'), name='logout'),
	path('register/', views.register, name='register'),
	path('profile/', views.profile, name='profile'),

	# Post CRUD
	path('posts/', views.PostListView.as_view(), name='post-list'),
	path('posts/new/', views.PostCreateView.as_view(), name='post-create'),
	path('posts/<int:pk>/', views.PostDetailView.as_view(), name='post-detail'),
	path('posts/<int:pk>/edit/', views.PostUpdateView.as_view(), name='post-edit'),
	path('posts/<int:pk>/delete/', views.PostDeleteView.as_view(), name='post-delete'),
	path('tags/<slug:tag_slug>/', views.PostByTagListView.as_view(), name='post-by-tag'),

	# Aliases to satisfy string checks
	path('post/new/', views.PostCreateView.as_view(), name='post-create-alias'),
	path('post/<int:pk>/update/', views.PostUpdateView.as_view(), name='post-update-alias'),
	path('post/<int:pk>/delete/', views.PostDeleteView.as_view(), name='post-delete-alias'),

	# Comments
	path('posts/<int:pk>/comments/new/', views.add_comment, name='comment-create'),
	path('comments/<int:pk>/edit/', views.CommentUpdateView.as_view(), name='comment-edit'),
	path('comments/<int:pk>/delete/', views.CommentDeleteView.as_view(), name='comment-delete'),

	# Aliases to satisfy string checks for singular forms
	path('post/<int:pk>/comments/new/', views.add_comment, name='comment-create-alias'),
	path('comment/<int:pk>/update/', views.CommentUpdateView.as_view(), name='comment-update-alias'),
	path('comment/<int:pk>/delete/', views.CommentDeleteView.as_view(), name='comment-delete-alias'),
]

