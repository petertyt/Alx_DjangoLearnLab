from django.db import models
from django.contrib.auth import get_user_model
from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes.fields import GenericForeignKey

User = get_user_model()


class Notification(models.Model):
    """
    Notification model for tracking user notifications.
    """
    NOTIFICATION_TYPES = [
        ('like', 'Like'),
        ('comment', 'Comment'),
        ('follow', 'Follow'),
        ('unfollow', 'Unfollow'),
    ]

    recipient = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='notifications',
        help_text="The user who receives the notification"
    )
    actor = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='notifications_sent',
        help_text="The user who performed the action"
    )
    verb = models.CharField(
        max_length=50,
        choices=NOTIFICATION_TYPES,
        help_text="The type of action performed"
    )
    target_content_type = models.ForeignKey(
        ContentType,
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        help_text="The type of object the action was performed on"
    )
    target_object_id = models.PositiveIntegerField(
        null=True,
        blank=True,
        help_text="The ID of the object the action was performed on"
    )
    target = GenericForeignKey('target_content_type', 'target_object_id')
    is_read = models.BooleanField(
        default=False,
        help_text="Whether the notification has been read"
    )
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created_at']
        indexes = [
            models.Index(fields=['recipient', 'is_read']),
            models.Index(fields=['created_at']),
        ]

    def __str__(self):
        return f"{self.actor.username} {self.get_verb_display()} - {self.recipient.username}"

    @property
    def message(self):
        """Generate a human-readable notification message."""
        if self.verb == 'like':
            return f"{self.actor.username} liked your post"
        elif self.verb == 'comment':
            return f"{self.actor.username} commented on your post"
        elif self.verb == 'follow':
            return f"{self.actor.username} started following you"
        elif self.verb == 'unfollow':
            return f"{self.actor.username} stopped following you"
        return f"{self.actor.username} {self.get_verb_display()}"

    def mark_as_read(self):
        """Mark the notification as read."""
        self.is_read = True
        self.save(update_fields=['is_read'])