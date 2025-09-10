from django.contrib import admin
from .models import Notification


@admin.register(Notification)
class NotificationAdmin(admin.ModelAdmin):
    """
    Admin configuration for Notification model.
    """
    list_display = ('recipient', 'actor', 'verb', 'is_read', 'created_at')
    list_filter = ('is_read', 'verb', 'created_at', 'recipient', 'actor')
    search_fields = ('recipient__username', 'actor__username', 'verb')
    ordering = ('-created_at',)
    readonly_fields = ('created_at',)
    
    fieldsets = (
        ('Notification Information', {
            'fields': ('recipient', 'actor', 'verb', 'is_read')
        }),
        ('Target Object', {
            'fields': ('target_content_type', 'target_object_id'),
            'classes': ('collapse',)
        }),
        ('Timestamps', {
            'fields': ('created_at',),
            'classes': ('collapse',)
        }),
    )
    
    actions = ['mark_as_read', 'mark_as_unread']
    
    def mark_as_read(self, request, queryset):
        """Mark selected notifications as read."""
        updated = queryset.update(is_read=True)
        self.message_user(request, f'{updated} notifications marked as read.')
    mark_as_read.short_description = "Mark selected notifications as read"
    
    def mark_as_unread(self, request, queryset):
        """Mark selected notifications as unread."""
        updated = queryset.update(is_read=False)
        self.message_user(request, f'{updated} notifications marked as unread.')
    mark_as_unread.short_description = "Mark selected notifications as unread"