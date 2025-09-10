from django.contrib import admin
from .models import Post, Comment


@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    """
    Admin configuration for Post model.
    """
    list_display = ('title', 'author', 'created_at', 'likes_count', 'comments_count')
    list_filter = ('created_at', 'updated_at', 'author')
    search_fields = ('title', 'content', 'author__username')
    ordering = ('-created_at',)
    readonly_fields = ('created_at', 'updated_at', 'likes_count', 'comments_count')
    
    fieldsets = (
        ('Post Information', {
            'fields': ('author', 'title', 'content')
        }),
        ('Timestamps', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
        ('Statistics', {
            'fields': ('likes_count', 'comments_count'),
            'classes': ('collapse',)
        }),
    )


@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    """
    Admin configuration for Comment model.
    """
    list_display = ('post', 'author', 'created_at', 'likes_count')
    list_filter = ('created_at', 'updated_at', 'author', 'post')
    search_fields = ('content', 'author__username', 'post__title')
    ordering = ('-created_at',)
    readonly_fields = ('created_at', 'updated_at', 'likes_count')
    
    fieldsets = (
        ('Comment Information', {
            'fields': ('post', 'author', 'content')
        }),
        ('Timestamps', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
        ('Statistics', {
            'fields': ('likes_count',),
            'classes': ('collapse',)
        }),
    )